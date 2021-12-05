from tap_apple_search_ads.stream import core as stream


def test_metadata_disabled():
    metadata = stream.Metadata.disabled()
    assert metadata.selected is False
    assert metadata.breadcrumb == tuple()


def test_metadata_dict():
    metadata = stream.Metadata(True, ("properties", "test"))
    expected = {"metadata": {"selected": True}, "breadcrumb": ["properties", "test"]}
    assert metadata.dict() == expected


def test_metadata_dict_disabled():
    metadata = stream.Metadata.disabled()
    expected = {"metadata": {"selected": False}, "breadcrumb": []}
    assert metadata.dict() == expected
