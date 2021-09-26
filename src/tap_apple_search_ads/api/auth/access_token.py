from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Tuple

import requests
import singer

logger = singer.get_logger()


@dataclass
class AccessTokenValue:
    access_token: str
    token_type: str
    expires_in: int

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AccessTokenValue":
        return cls(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
        )

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AccessToken:
    client_id: str
    client_secret: str
    url: str = "https://appleid.apple.com/auth/oauth2/token"

    @property
    def value(self) -> AccessTokenValue:
        logger.debug(
            "url: [%s], headers: [%s], params: [%s]",
            self.url,
            self.headers,
            self.params,
        )

        response = requests.post(
            self.url,
            headers=self.headers,
            params=self.params,
        )

        data = response.json()

        return AccessTokenValue.from_mapping(data)

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Host": "appleid.apple.com",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    @property
    def params(self) -> Tuple[Tuple[str, str], ...]:
        return (
            ("client_id", self.client_id),
            ("client_secret", self.client_secret),
            ("grant_type", "client_credentials"),
            ("scope", "searchadsorg"),
        )
