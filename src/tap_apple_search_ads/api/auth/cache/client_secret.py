from typing import Any, MutableMapping, Optional, Union

import singer
from tap_apple_search_ads.api.auth import client_secret
from tap_apple_search_ads.api.auth.cache import utils

logger = singer.get_logger()


class ClientSecret(client_secret.ClientSecret):
    def __init__(
        self,
        client_secret: client_secret.ClientSecret,
        cache: MutableMapping[str, Any],
        expiration_time: int = 3600,
        cache_key: str = "client_secret_value",
    ) -> None:
        self.client_secret = client_secret
        self.cache = cache

        self.expiration_time = expiration_time
        self.cache_key = cache_key

    def value(self, private_key: str) -> str:
        value_ = self.maybe_get()
        if value_:
            return value_

        value_ = self.client_secret.value(private_key)

        self.put(value_)

        return value_

    def maybe_get(
        self, request_time: Optional[Union[float, int]] = None
    ) -> Optional[str]:
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
        value: str,
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
        return "Cached({})".format(repr(self.client_secret))
