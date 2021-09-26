import datetime
import pathlib
import shelve
from typing import Any, List, Mapping, MutableMapping

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


def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    private_key = load_private_key(args.config)

    now = datetime.datetime.now(tz=pytz.utc)
    timestamp = int(now.timestamp())

    config_ = config.Authentication(args.config)

    request_headers = set_up_authentication(private_key, timestamp, config_)

    return request_headers


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
    private_key: str, timestamp: int, config_: config.Authentication
) -> auth.RequestHeaders:
    cache_file_path = pathlib.Path(config_.tmp_dir) / config_.auth_cache_file
    cache = shelve.open(cache_file_path.as_posix())

    try:
        return set_up_cached_auth(private_key, timestamp, config_, cache)

    finally:
        cache.close()


def set_up_cached_auth(
    private_key: str,
    timestamp: int,
    config_: config.Authentication,
    cache: MutableMapping[str, Any],
):
    headers = client_secret.Headers(config_.key_id, config_.algorithm)
    payload = client_secret.Payload(
        config_.client_id, config_.team_id, config_.audience
    )
    client_secret_ = auth.ClientSecret(
        timestamp, config_.expiration_time, private_key, headers, payload
    )
    client_secret_ = auth.cache.ClientSecret(client_secret_, cache)

    access_token = auth.AccessToken(
        config_.client_id, client_secret_.value, config_.url
    )
    access_token = auth.cache.AccessToken(access_token, cache)

    request_headers = auth.RequestHeaders(config_.org_id, access_token.value)
    request_headers = auth.cache.RequestHeaders(request_headers, cache)

    return request_headers
