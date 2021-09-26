import datetime
import pathlib
import shelve
from typing import Any, List, Mapping, MutableMapping, Optional, Tuple

import pytz
import singer

from tap_apple_search_ads import config
from tap_apple_search_ads.api import auth
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

cache: Optional[shelve.Shelf] = None


def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    now = datetime.datetime.now(tz=pytz.utc)
    timestamp = int(now.timestamp())

    config_ = config.Authentication(args.config)

    auth_objects = set_up_authentication(timestamp, config_)

    if config_.local_caching:
        cache = get_or_create_cache(config_.tmp_dir, config_.auth_cache_file)
        auth_objects = add_caching(*auth_objects, cache=cache)

    private_key = load_private_key(args.config)

    request_headers_value = authenticate(*request_headers)

    return (private_key, *auth_objects)


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
    config_: config.Authentication,
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

    return (client_secret_, access_token, request_headers)


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
