import tap_apple_search_ads as tap
from tap_apple_search_ads.stream.core import Descriptor


def test_add_selector_name():
    descriptor = Descriptor("test", "test", {}, [])
    new_descriptor = tap.add_selector_name(descriptor, "groupby_day")
    assert new_descriptor.tap_stream_id == "test_groupby_day"
