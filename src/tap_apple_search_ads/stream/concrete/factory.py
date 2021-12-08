from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.core import Descriptor, Metadata

CAMPAIGN = "campaign"
CAMPAIGN_FLAT = "campaign_flat"
CAMPAIGN_LEVEL_REPORTS = "campaign_level_reports"
CAMPAIGN_LEVEL_REPORTS_ESR = "campaign_level_reports_extended_spend_row"
CAMPAIGN_LEVEL_REPORTS_ESR_FLAT = "campaign_level_reports_extended_spend_row_flat"


class SchemasProvider(Protocol):
    def campaign(self) -> Schema:
        ...

    def campaign_flat(self) -> Schema:
        ...

    def campaign_level_reports(self) -> Schema:
        ...

    def campaign_level_reports_extended_spend_row(self) -> Schema:
        ...

    def campaign_level_reports_extended_spend_row_flat(self) -> Schema:
        ...


@dataclass
class DescriptorFactory:
    schemas: SchemasProvider

    def campaign(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN,
            tap_stream_id=CAMPAIGN,
            schema=self.schemas.campaign(),
            metadata=[Metadata.disabled()],
        )

    def campaign_flat(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN_FLAT,
            tap_stream_id=CAMPAIGN_FLAT,
            schema=self.schemas.campaign_flat(),
            metadata=[Metadata.disabled()],
        )

    def campaign_level_reports(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN_LEVEL_REPORTS,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS,
            schema=self.schemas.campaign_level_reports(),
            metadata=[Metadata.disabled()],
        )

    def campaign_level_reports_extended_spend_row(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN_LEVEL_REPORTS_ESR,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS_ESR,
            schema=self.schemas.campaign_level_reports_extended_spend_row(),
            metadata=[Metadata.disabled()],
        )

    def campaign_level_reports_extended_spend_row_flat(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN_LEVEL_REPORTS_ESR_FLAT,
            tap_stream_id=CAMPAIGN_LEVEL_REPORTS_ESR_FLAT,
            schema=self.schemas.campaign_level_reports_extended_spend_row_flat(),
            metadata=[Metadata.disabled()],
        )
