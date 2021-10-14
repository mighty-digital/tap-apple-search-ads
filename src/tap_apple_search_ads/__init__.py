import datetime
import json
import pathlib
import shelve
import sys
import time
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Tuple

import pytz
import singer

from tap_apple_search_ads import config as tap_config
from tap_apple_search_ads.api import auth, campaign
from tap_apple_search_ads.api.auth import client_secret

logger = singer.get_logger()

REQUIRED_CONFIG_KEYS: List[str] = [
    # ClientSecret
    "client_id",
    "team_id",
    "key_id",
    # RequestHeaders
    "org_id",
]

STREAMS = [
    "campaign",
    "campaign_level_reports"
]

cache: Optional[shelve.Shelf] = None


def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.discover:
        return do_discover()

    if args.catalog:
        return do_sync(args.config, args.catalog)


def do_discover() -> int:
    result: Dict[str, List[Dict[str, Any]]] = {"streams": []}

    for stream in STREAMS:
        schema = load_schema(stream)
        schema = singer.resolve_schema_references(schema)

        result["streams"].append(
            {
                "stream": stream,
                "tap_stream_id": stream,
                "schema": schema,
            }
        )

    json.dump(result, sys.stdout, indent=2)

    return 0


def load_schema(stream_name: str) -> Dict[str, Any]:
    path = (
        pathlib.Path(__file__).parent / "schemas" / "{}.json".format(stream_name)
    ).absolute()

    with open(path, "r") as stream:
        schema = json.load(stream)

    return schema


def do_sync(config: Dict[str, Any], catalog: singer.Catalog):
    now = datetime.datetime.now(tz=pytz.utc)
    timestamp = int(now.timestamp())

    config_ = tap_config.Authentication(config)

    auth_objects = set_up_authentication(timestamp, config_)

    if config_.local_caching:
        cache = get_or_create_cache(config_.tmp_dir, config_.auth_cache_file)
        auth_objects = add_caching(*auth_objects, cache=cache)

    cs, at, rh = auth_objects
    private_key = load_private_key(config)

    request_headers_value = rh.value(at.value(cs.value(private_key)))

    for stream in catalog.streams:
        stream_name = stream.tap_stream_id
        sync_stream(stream_name, stream, request_headers_value)

    logger.info("Done syncing.")

    return 0


def load_private_key(config: Mapping[str, str]) -> str:
    if "private_key_value" in config:
        private_key = config["private_key_value"]

    elif "private_key_path" in config:
        private_key_path = config["private_key_path"]
        private_key = auth.utils.read_private_key_from_file(private_key_path)

    else:
        raise TapAppleSearchAdsException("Missing private key configuration parameters")

    return private_key


class TapAppleSearchAdsException(Exception):
    pass


def set_up_authentication(
    timestamp: int,
    config_: tap_config.Authentication,
) -> Tuple[auth.ClientSecret, auth.AccessToken, auth.RequestHeaders]:
    headers = client_secret.Headers(config_.key_id, config_.algorithm)
    payload = client_secret.Payload(
        config_.client_id, config_.team_id, config_.audience
    )
    client_secret_ = auth.ClientSecret(
        timestamp, config_.expiration_time, headers, payload
    )

    access_token = auth.AccessToken(config_.client_id, config_.url)

    request_headers = auth.RequestHeaders(config_.org_id)

    return client_secret_, access_token, request_headers


def get_or_create_cache(cache_dir: str, cache_file: str) -> shelve.Shelf:
    global cache
    if cache:
        return cache

    cache_dir_ = pathlib.Path(cache_dir)

    if not cache_dir_.exists():
        raise OSError(
            "Cache directory [{}] does not exist".format(cache_dir_.as_posix())
        )

    cache_file_ = cache_dir_ / cache_file

    cache = shelve.open(cache_file_.as_posix())

    return cache


def add_caching(
    client_secret: auth.ClientSecret,
    access_token: auth.AccessToken,
    request_headers: auth.RequestHeaders,
    cache: MutableMapping[str, Any],
) -> Tuple[auth.ClientSecret, auth.AccessToken, auth.RequestHeaders]:
    return (
        auth.cache.ClientSecret(client_secret, cache),
        auth.cache.AccessToken(access_token, cache),
        auth.cache.RequestHeaders(request_headers, cache),
    )


def sync_stream(
    stream_name: str, stream: singer.CatalogEntry, headers: auth.RequestHeadersValue
) -> None:
    start_time = time.monotonic()
    logger.info("%s: Starting sync", stream_name)
    singer.write_schema(stream_name, stream.schema.to_dict(), [])

    count = sync_concrete_stream(stream_name, headers)

    end_time = time.monotonic() - start_time
    logger.info(
        "%s: Completed sync (%s rows) in %s seconds", stream_name, count, end_time
    )


def sync_concrete_stream(stream_name: str, headers: auth.RequestHeadersValue) -> int:
    if stream_name == "campaign":
        campaing_records = campaign.sync(headers)
        for record in campaing_records:
            record = campaign.to_schema(record)
            singer.write_record(stream_name, record)

        return len(campaing_records)

    elif stream_name == "campaign_level_reports":
        reports_records = campaign_level_reports.sync(headers)
        for record in reports_records:
            # record = campaign_level_reports.to_schema(record)
            singer.write_record(stream_name, record)
        
        return len(reports_records)

    raise TapAppleSearchAdsException("Unknown stream: [{}]".format(stream_name))
