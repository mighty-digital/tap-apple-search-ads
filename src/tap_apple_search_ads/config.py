from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Authentication:
    # authentication
    key_id: str
    client_id: str
    team_id: str
    org_id: str

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
