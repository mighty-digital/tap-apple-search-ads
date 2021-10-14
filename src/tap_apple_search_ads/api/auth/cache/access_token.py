from typing import Any, MutableMapping, Optional, Union

import singer

from tap_apple_search_ads.api.auth import access_token
from tap_apple_search_ads.api.auth.cache import utils

logger = singer.get_logger()


class AccessToken(access_token.AccessToken):
    def __init__(
        self,
        access_token: access_token.AccessToken,
        cache: MutableMapping[str, Any],
        expiration_time: int = 3600,
        cache_key: str = "access_token_value",
    ) -> None:
        """cache.AccessToken provides cached variant of an AccessToken class. Responses
        are cached in provided MutableMapping to instead of performing request every
        time.

        Parameters
        ----------
        access_token : access_token.AccessToken
            AccessToken object to decorate, in case of cache miss request will be
            redirected to it.
        cache : MutableMapping[str, Any]
            cache object used for value cahcing
        expiration_time : int, optional
            how long cached value remains valid, in seconds, by default 3600
        """

        self.access_token = access_token
        self.cache = cache

        self.expiration_time = expiration_time
        self.cache_key = cache_key

    def value(self, client_secret: str) -> access_token.AccessTokenValue:
        value_ = self.maybe_get()
        if value_:
            return value_

        value_ = self.access_token.value(client_secret)

        self.put(value_)

        return value_

    def maybe_get(
        self, request_time: Optional[Union[float, int]] = None
    ) -> Optional[access_token.AccessTokenValue]:
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

        return access_token.AccessTokenValue.from_mapping(data)

    def put(
        self,
        value: access_token.AccessTokenValue,
        request_time: Optional[Union[float, int]] = None,
    ) -> None:
        if request_time is None:
            request_time = utils.now()

        expiration_time = request_time + self.expiration_time
        value_ = value.asdict()

        logger.debug(
            "storing key [%s] with expiration time [%s]",
            self.cache_key,
            expiration_time,
        )

        self.cache[self.cache_key] = (expiration_time, value_)

    def __repr__(self) -> str:
        return "Cached({})".format(repr(self.access_token))
