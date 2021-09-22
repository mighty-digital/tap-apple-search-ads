"""Authorization in Apple Search Ads API."""

from tap_apple_search_ads.api.auth import utils
from tap_apple_search_ads.api.auth.access_token import AccessToken
from tap_apple_search_ads.api.auth.client_secret import ClientSecret
from tap_apple_search_ads.api.auth.request_headers import RequestHeaders

__all__ = [
    "utils",
    "AccessToken",
    "ClientSecret",
    "RequestHeaders",
]
