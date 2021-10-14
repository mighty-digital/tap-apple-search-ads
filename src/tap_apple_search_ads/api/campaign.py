"""Get All Campaigns stream"""

from typing import Any, Dict, List

import requests
import singer

from tap_apple_search_ads import api
from tap_apple_search_ads.api.auth import RequestHeadersValue

logger = singer.get_logger()

DEFAULT_URL = "https://api.searchads.apple.com/api/v4/campaigns"


def sync(headers: RequestHeadersValue) -> List[Dict[str, Any]]:
    logger.info("Sync: campaigns")

    response = requests.get(DEFAULT_URL, headers=headers)
    api.utils.check_response(response)
    campaigns = response.json()["data"]

    logger.info("Synced [%s] campaings", len(campaigns))

    return campaigns
