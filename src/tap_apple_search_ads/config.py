from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

import pytz
import singer

from tap_apple_search_ads.api import API_DATE_FORMAT

logger = singer.get_logger()


@dataclass
class Authentication:
    # authentication
    key_id: str
    client_id: str
    team_id: str
    org_id: str

    # vars
    start_time: str
    end_time: str

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

        # load vars
        if "start_time" in context:
            self.start_time = context["start_time"]
            if not self.start_time:
                logger.info("start_time value should not be empty")

        if "end_time" in context:
            self.end_time = context["end_time"]
            if not self.end_time:
                self.end_time = datetime.now(tz=pytz.utc).strftime(API_DATE_FORMAT)
