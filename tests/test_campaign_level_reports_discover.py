import pytest

from tap_apple_search_ads.api import campaign_level_reports


@pytest.mark.xfail("Example test to be removed")
def test_stream_discovery():
    config = {
        "campaign_level_reports": {
            "selectors": {
                "a": {},
                "b": {},
                "c": {},
            }
        }
    }

    discovered_streams = campaign_level_reports.discover_streams(config)  # noqa

    assert discovered_streams == [
        {"stream_name": "campaign_level_reports__a"},
        {"stream_name": "campaign_level_reports__b"},
        {"stream_name": "campaign_level_reports__c"},
    ]
