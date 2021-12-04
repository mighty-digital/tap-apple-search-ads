from tap_apple_search_ads.stream import api


def test_metadata_disabled():
    metadata = api.Metadata.disabled()
    assert metadata.enabled is False
    assert metadata.breadcrumb == tuple()
