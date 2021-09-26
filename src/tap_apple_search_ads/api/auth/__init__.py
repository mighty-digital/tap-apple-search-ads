"""Authorization in Apple Search Ads API."""

from tap_apple_search_ads.api.auth import cache, utils
from tap_apple_search_ads.api.auth.access_token import AccessToken
from tap_apple_search_ads.api.auth.client_secret import ClientSecret
from tap_apple_search_ads.api.auth.request_headers import RequestHeaders

__all__ = [
    "cache",
    "utils",
    "AccessToken",
    "ClientSecret",
    "RequestHeaders",
]
