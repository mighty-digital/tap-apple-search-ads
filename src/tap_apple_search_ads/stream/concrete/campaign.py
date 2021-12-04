import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Protocol, TypedDict

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream import Record, StreamError

from .base import ConcreteStreamBase

CAMPAIGN = "campaign"
CAMPAIGN_FLAT = "campaign_flat"

PROPERTIES_TO_SERIALIZE = {
    "budgetOrders",
    "countriesOrRegions",
    "countryOrRegionServingStateReasons",
    "locInvoiceDetails",
    "servingStateReasons",
    "supplySources",
}


class CampaignSchemaProvider(Protocol):
    def campaign(self) -> Schema:
        ...


GetAllCampaignsResponse = TypedDict(
    "GetAllCampaignsResponse", {"data": List[Dict[str, Any]]}
)


class GetAllCampaigns(Protocol):
    def get_all_campaigns(self) -> GetAllCampaignsResponse:
        ...


@dataclass
class Campaign(ConcreteStreamBase):
    _api: Optional[GetAllCampaigns] = field(init=False, default=None)

    @classmethod
    def from_schema_provider(cls, provider: CampaignSchemaProvider):
        return cls(stream=CAMPAIGN, tap_stream_id=CAMPAIGN, schema=provider.campaign())

    def set_api(self, api: GetAllCampaigns):
        self._api = api

    @property
    def api(self):
        if self._api is None:
            raise StreamError(
                "API is not set for Stream [{}]".format(self.descriptor())
            )

        return self._api

    def sync(self) -> Iterable[Record]:
        data = self.api.get_all_campaigns()
        records = data["data"]
        return records


class CampaignFlatSchemaProvider(Protocol):
    def campaign_flat(self) -> Schema:
        ...


@dataclass
class CampaignFlat(ConcreteStreamBase):
    _campaign: Optional[Campaign] = field(init=False, default=None)

    @classmethod
    def from_schema_provider(cls, provider: CampaignFlatSchemaProvider):
        return cls(
            stream=CAMPAIGN_FLAT,
            tap_stream_id=CAMPAIGN_FLAT,
            schema=provider.campaign_flat(),
        )

    def set_campaign(self, campaign: Campaign):
        self._campaign = campaign

    @property
    def campaign(self) -> Campaign:
        if self._campaign is None:
            raise StreamError(
                "Campaign instance is not set for Stream [{}]".format(self.descriptor())
            )

        return self._campaign

    def sync(self) -> Iterable[Record]:
        records: List[Record] = []
        for record in self.campaign.sync():
            records.append(flatten(record))
        return records


def flatten(record: Record) -> Record:
    budgetAmount = record.pop("budgetAmount")

    record["budgetAmount_currency"] = budgetAmount["currency"]
    record["budgetAmount_amount"] = budgetAmount["amount"]

    dailyBudgetAmount = record.pop("dailyBudgetAmount")

    record["dailyBudgetAmount_currency"] = dailyBudgetAmount["currency"]
    record["dailyBudgetAmount_amount"] = dailyBudgetAmount["amount"]

    for key in PROPERTIES_TO_SERIALIZE:
        value = record.pop(key)
        record[key] = serialize(value)

    return record


def serialize(value: Any) -> Optional[str]:
    if value is None:
        return None

    value_str = json.dumps(value)

    return value_str
