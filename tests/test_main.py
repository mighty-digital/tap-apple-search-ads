import unittest
from typing import Optional

import tap_apple_search_ads as tap
from tap_apple_search_ads.stream.concrete import DescriptorFactory
from tap_apple_search_ads.stream.core import Descriptor


def assert_count_equal(first, second):
    tester = unittest.TestCase()
    tester.maxDiff = None
    tester.assertCountEqual(first, second)


def descriptor(stream: str, tap_stream_id: Optional[str] = None) -> Descriptor:
    return Descriptor(stream, tap_stream_id or stream, {}, [])


class MockDescriptorFactory(DescriptorFactory):
    def __init__(self) -> None:
        pass

    def campaign(self) -> Descriptor:
        return descriptor("campaign")

    def campaign_flat(self) -> Descriptor:
        return descriptor("campaign_flat")

    def campaign_level_reports(self) -> Descriptor:
        return descriptor("campaign_level_reports")

    def campaign_level_reports_extended_spend_row(self) -> Descriptor:
        return descriptor("campaign_level_reports_extended_spend_row")

    def campaign_level_reports_extended_spend_row_flat(self) -> Descriptor:
        return descriptor("campaign_level_reports_extended_spend_row_flat")


def test_create_default_descriptors():
    assert_count_equal(
        tap.create_default_descriptors(MockDescriptorFactory()),
        [
            descriptor("campaign"),
            descriptor("campaign_flat"),
            descriptor("campaign_level_reports"),
            descriptor("campaign_level_reports_extended_spend_row"),
            descriptor("campaign_level_reports_extended_spend_row_flat"),
        ],
    )


def test_add_selector_name():
    descriptor = Descriptor("test", "test", {}, [])
    new_descriptor = tap.add_selector_name(descriptor, "groupby_day")
    assert new_descriptor.tap_stream_id == "test_groupby_day"


def test_create_dynamic_descriptors():
    config = {
        "selectors": {
            "0": {},
            "1": {},
            "2": {},
        }
    }

    assert_count_equal(
        tap.create_dynamic_descriptors(config, MockDescriptorFactory()),
        [
            descriptor("campaign_level_reports", "campaign_level_reports_0"),
            descriptor(
                "campaign_level_reports_extended_spend_row",
                "campaign_level_reports_extended_spend_row_0",
            ),
            descriptor(
                "campaign_level_reports_extended_spend_row_flat",
                "campaign_level_reports_extended_spend_row_flat_0",
            ),
            descriptor("campaign_level_reports", "campaign_level_reports_1"),
            descriptor(
                "campaign_level_reports_extended_spend_row",
                "campaign_level_reports_extended_spend_row_1",
            ),
            descriptor(
                "campaign_level_reports_extended_spend_row_flat",
                "campaign_level_reports_extended_spend_row_flat_1",
            ),
            descriptor("campaign_level_reports", "campaign_level_reports_2"),
            descriptor(
                "campaign_level_reports_extended_spend_row",
                "campaign_level_reports_extended_spend_row_2",
            ),
            descriptor(
                "campaign_level_reports_extended_spend_row_flat",
                "campaign_level_reports_extended_spend_row_flat_2",
            ),
        ],
    )
