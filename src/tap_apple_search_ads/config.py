from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Mapping

import pytz
import singer

logger = singer.get_logger()


def default_start_time() -> datetime:
    now = datetime.now(tz=pytz.utc)
    start_time = datetime(now.year, now.month, now.day)
    return start_time


def default_end_time() -> datetime:
    now = datetime.now(tz=pytz.utc)
    end_time = datetime(now.year, now.month, now.day) + timedelta(days=1)
    return end_time


@dataclass
class Authentication:
    # authentication
    key_id: str
    client_id: str
    team_id: str
    org_id: str

    # selector parameters
    start_time: datetime = field(default_factory=default_start_time)
    end_time: datetime = field(default_factory=default_end_time)

    # authentication
    algorithm: str = "ES256"
    audience: str = "https://appleid.apple.com"
    expiration_time: int = 3600
    url: str = "https://appleid.apple.com/auth/oauth2/token"

    # caching
    local_caching: bool = False
    tmp_dir: str = "tmp"
    auth_cache_file: str = "auth"

    def __init__(self, context: Mapping[str, Any]) -> None:
        self.key_id = context["key_id"]
        self.client_id = context["client_id"]
        self.team_id = context["team_id"]
        self.org_id = context["org_id"]

        if "algorithm" in context:
            self.algorithm = context["algorithm"]
        if "audience" in context:
            self.audience = context["audience"]
        if "expiration_time" in context:
            self.expiration_time = context["expiration_time"]
        if "url" in context:
            self.url = context["url"]

        if "local_caching" in context:
            self.local_caching = context["local_caching"]
        if "tmp_dir" in context:
            self.tmp_dir = context["tmp_dir"]
        if "auth_cache_file" in context:
            self.auth_cache_file = context["auth_cache_file"]

        if "start_time" in context:
            start_time_str = context["start_time"]
            if start_time_str:
                self.start_time = datetime.fromisoformat(start_time_str).replace(
                    tzinfo=pytz.utc
                )

        if "end_time" in context:
            end_time_str = context["end_time"]
            if end_time_str:
                self.end_time = datetime.fromisoformat(end_time_str).replace(
                    tzinfo=pytz.utc
                )
