import datetime
from dataclasses import asdict, dataclass
from typing import ClassVar

import jwt
import singer

logger = singer.get_logger()


@dataclass
class Payload:
    client_id: str
    team_id: str
    audience: str = "https://appleid.apple.com"


@dataclass
class Headers:
    key_id: str
    algorithm: str = "ES256"


@dataclass
class ClientSecret:
    issued_at_timestamp: int
    expiration_time: int
    headers: Headers
    payload: Payload

    _max_expiration_time: ClassVar[float] = datetime.timedelta(days=180).total_seconds()

    @property
    def expiration_timestamp(self) -> int:

        if self.expiration_time > self._max_expiration_time:
            raise ValueError(
                (
                    "expiration_time ([{}] seconds) may not exceed 180 days "
                    "from issue timestamp ([{}] seconds)"
                ).format(self.expiration_time, self._max_expiration_time)
            )

        return self.issued_at_timestamp + self.expiration_time

    def value(self, private_key: str) -> str:
        jwt_payload = asdict(
            JwtPayload(
                sub=self.payload.client_id,
                aud=self.payload.audience,
                iat=self.issued_at_timestamp,
                exp=self.expiration_timestamp,
                iss=self.payload.team_id,
            )
        )

        jwt_headers = asdict(
            JwtHeaders(
                alg=self.headers.algorithm,
                kid=self.headers.key_id,
            )
        )

        logger.debug(
            "payload: [%s], headers: [%s], algorithm: [%s]",
            self.payload,
            self.headers,
            self.headers.algorithm,
        )

        client_secret = jwt.encode(
            payload=jwt_payload,
            headers=jwt_headers,
            algorithm=self.headers.algorithm,
            key=private_key,
        )

        return client_secret


@dataclass
class JwtPayload:
    sub: str
    aud: str
    iat: int
    exp: int
    iss: str


@dataclass
class JwtHeaders:
    alg: str
    kid: str
