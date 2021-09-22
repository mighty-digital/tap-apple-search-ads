from dataclasses import dataclass
from typing import TypedDict

import singer
from tap_apple_search_ads.api.auth.access_token import AccessTokenValue

logger = singer.get_logger()

RequestHeadersValue = TypedDict(
    "RequestHeadersValue",
    {
        "Authorization": str,
        "X-AP-Context": str,
    },
)


@dataclass
class RequestHeaders:
    org_id: str
    access_token: AccessTokenValue

    @property
    def value(self) -> RequestHeadersValue:
        if self.access_token.token_type != "Bearer":
            message = "Unexpected token_type [{}], expected Bearer"
            logger.error(message, self.access_token.token_type)
            raise RuntimeError(message.format(self.access_token.token_type))

        return {
            "Authorization": "{} {}".format(
                self.access_token.token_type, self.access_token.access_token
            ),
            "X-AP-Context": "orgId={}".format(self.org_id),
        }
