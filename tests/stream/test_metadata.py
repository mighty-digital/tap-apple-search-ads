from tap_apple_search_ads.stream import api


def test_metadata_disabled():
    metadata = api.Metadata.disabled()
    assert metadata.selected is False
    assert metadata.breadcrumb == tuple()


def test_metadata_dict():
    metadata = api.Metadata(True, ("properties", "test"))
    expected = {"metadata": {"selected": True}, "breadcrumb": ["properties", "test"]}
    assert metadata.dict() == expected


def test_metadata_dict_disabled():
    metadata = api.Metadata.disabled()
    expected = {"metadata": {"selected": False}, "breadcrumb": []}
    assert metadata.dict() == expected
