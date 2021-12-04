from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema

from .core import ConcreteStreamBase

CAMPAIGN_LEVEL_REPORTS = "campaign_level_reports"
CAMPAIGN_LEVEL_REPORTS_ESR = "campaign_level_reports_extended_spend_row"
CAMPAIGN_LEVEL_REPORTS_ESR_FLAT = "campaign_level_reports_extended_spend_row_flat"


class ClrSchemaProvider(Protocol):
    def campaign_level_reports(self) -> Schema:
        ...


@dataclass
class CampaignLevelReports(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: ClrSchemaProvider):
        return cls(
            stream=CAMPAIGN_LEVEL_REPORTS,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS,
            schema=provider.campaign_level_reports(),
        )


class EsrSchemaProvider(Protocol):
    def campaign_level_reports_extended_spend_row(self) -> Schema:
        ...


@dataclass
class ExtendedSpendRow(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: EsrSchemaProvider):
        return cls(
            stream=CAMPAIGN_LEVEL_REPORTS_ESR,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS_ESR,
            schema=provider.campaign_level_reports_extended_spend_row(),
        )


class EsrFlatSchemaProvider(Protocol):
    def campaign_level_reports_extended_spend_row_flat(self) -> Schema:
        ...


@dataclass
class ExtendedSpendRowFlat(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: EsrFlatSchemaProvider):
        return cls(
            stream=CAMPAIGN_LEVEL_REPORTS_ESR_FLAT,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS_ESR_FLAT,
            schema=provider.campaign_level_reports_extended_spend_row_flat(),
        )
