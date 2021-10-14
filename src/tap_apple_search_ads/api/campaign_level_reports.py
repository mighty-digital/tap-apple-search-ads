"""Campaign Level Reports"""

from typing import Any, Dict, List


import json
import pathlib
import requests
import singer
from tap_apple_search_ads.api.auth import RequestHeadersValue
from tap_apple_search_ads import api
import datetime

logger = singer.get_logger()

DEFAULT_URL = "https://api.searchads.apple.com/api/v4/reports/campaigns"

reportsSelector = {
    "loaded": False, 
    "data": {}
}


def load_selector(path: str):
    
    f = open(path, 'r')
    
    reportsSelector["loaded"] = True
    reportsSelector["data"] = json.load(f)
    
    f.close()

def sync(headers: RequestHeadersValue) -> List[Dict[str, Any]]: 

    if reportsSelector["loaded"] == False:
        path = (
        pathlib.Path(__file__).parent / "../selectors" / "reports_selector.json"
    ).absolute()
        load_selector(path)

    
    logger.info("Sync: campaign level reports")
    response = requests.post(DEFAULT_URL, headers=headers, json=reportsSelector["data"])
    api.utils.check_response(response)
    print(response.json()["data"])
    return response.json()["data"]["reportingDataResponse"]["row"]

# todo
def to_schema(record: Dict[str, Any]) -> Dict[str, Any]:

    total = record.pop("total")
    avgCPA = total.pop("avgCPA")

    record["avgCPA.__currency"] = avgCPA["currency"]
    record["avgCPA.__amount"] = avgCPA["amount"]

    return record
