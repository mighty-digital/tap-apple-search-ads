"""Campaign Level Reports"""

import json
import pathlib
from datetime import datetime
from typing import Any, Dict, List

import requests
import singer

from tap_apple_search_ads import api
from tap_apple_search_ads.api.auth import RequestHeadersValue

logger = singer.get_logger()

DEFAULT_URL = "https://api.searchads.apple.com/api/v4/reports/campaigns"

reportsSelector: Dict[str, Any] = {"loaded": False, "data": Dict[str, Any]}


def load_selector(path: str):

    with open(path, "r") as stream:
        reportsSelector["loaded"] = True
        reportsSelector["data"] = json.load(stream)


def sync(
    headers: RequestHeadersValue, start_time: datetime, end_time: datetime
) -> List[Dict[str, Any]]:

    if not reportsSelector["loaded"]:
        path = (
            (pathlib.Path(__file__).parent / "../selectors" / "reports_selector.json")
            .absolute()
            .as_posix()
        )
        load_selector(path)

    selector = reportsSelector["data"]

    selector["startTime"] = start_time.strftime(api.API_DATE_FORMAT)
    selector["endTime"] = end_time.strftime(api.API_DATE_FORMAT)

    logger.info(
        "Sync: campaign level reports with start time [%s] and end time [%s]",
        start_time,
        end_time,
    )

    response = requests.post(DEFAULT_URL, headers=headers, json=selector)
    api.utils.check_response(response)

    # print will pollute stdout and fail downstream targets
    logger.debug(response.json()["data"])

    return response.json()["data"]["reportingDataResponse"]["row"]
