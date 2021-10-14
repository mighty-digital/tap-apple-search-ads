"""Get All Campaigns stream"""

import json
from typing import Any, Dict, List

import requests
import singer

from tap_apple_search_ads import api
from tap_apple_search_ads.api.auth import RequestHeadersValue

logger = singer.get_logger()

DEFAULT_URL = "https://api.searchads.apple.com/api/v4/campaigns"


# might have missed something
to_serialize = {
    "locInvoiceDetails",
    "budgetOrders",
    "countriesOrRegions",
    "servingStateReasons",
    "supplySources",
    "countryOrRegionServingStateReasons",
}


def sync(headers: RequestHeadersValue) -> List[Dict[str, Any]]:
    logger.info("Sync: campaigns")
    response = requests.get(DEFAULT_URL, headers=headers)
    api.utils.check_response(response)
    campaigns = response.json()["data"]
    logger.info("Synced [%s] campaings", len(campaigns))
    return campaigns


def to_schema(record: Dict[str, Any]) -> Dict[str, Any]:
    dailyBudgetAmount = record.pop("dailyBudgetAmount")

    record["dailyBudgetAmount.__currency"] = dailyBudgetAmount["currency"]
    record["dailyBudgetAmount.__amount"] = dailyBudgetAmount["amount"]

    budgetAmount = record.pop("budgetAmount")

    record["budgetAmount.__currency"] = budgetAmount["currency"]
    record["budgetAmount.__amount"] = budgetAmount["amount"]

    for v in to_serialize:
        serialize(record, v)

    return record


def serialize(record: Dict[str, Any], w: str):
    obj = record.pop(w)
    obj = json.dumps(obj)

    record[w] = obj
