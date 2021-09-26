from typing import Any, MutableMapping, Optional, Union

import singer
from tap_apple_search_ads.api.auth import request_headers, access_token
from tap_apple_search_ads.api.auth.cache import utils

logger = singer.get_logger()


class RequestHeaders(request_headers.RequestHeaders):
    def __init__(
        self,
        request_headers: request_headers.RequestHeaders,
        cache: MutableMapping[str, Any],
        expiration_time: int = 3600,
        cache_key: str = "client_secret_value",
    ) -> None:
        self.request_headers = request_headers
        self.cache = cache

        self.expiration_time = expiration_time
        self.cache_key = cache_key

    def value(
        self, access_token: access_token.AccessTokenValue
    ) -> request_headers.RequestHeadersValue:
        value_ = self.maybe_get()
        if value_:
            return value_

        value_ = self.request_headers.value(access_token)

        self.put(value_)

        return value_

    def maybe_get(
        self, request_time: Optional[Union[float, int]] = None
    ) -> Optional[request_headers.RequestHeadersValue]:
        if self.cache_key not in self.cache:
            return None

        expiration_time, data = self.cache[self.cache_key]

        if request_time is None:
            request_time = utils.now()

        if request_time > expiration_time:
            logger.debug(
                (
                    "value for key [%s] is expired "
                    "(request_time [%s] > expiration_time [%s])"
                ),
                self.cache_key,
                request_time,
                expiration_time,
            )

            return None

        logger.debug("hit key [%s]", self.cache_key)

        return data

    def put(
        self,
        value: request_headers.RequestHeadersValue,
        request_time: Optional[Union[float, int]] = None,
    ) -> None:
        if request_time is None:
            request_time = utils.now()

        expiration_time = request_time + self.expiration_time

        logger.debug(
            "storing key [%s] with expiration time [%s]",
            self.cache_key,
            expiration_time,
        )

        self.cache[self.cache_key] = (expiration_time, value)

    def __repr__(self) -> str:
        return "Cached({})".format(repr(self.request_headers))
