from tap_apple_search_ads.stream import api


def test_descriptor_disabled():
    descriptor = api.Descriptor.disabled(
        stream="test",
        schema={"type": "object"},
    )

    assert descriptor.stream == "test"
    assert descriptor.tap_stream_id == "test"
    assert descriptor.schema == {"type": "object"}
    assert len(descriptor.metadata) == 1
    assert descriptor.metadata[0] == api.Metadata.disabled()


def test_descriptor_disabled_dict():
    descriptor = api.Descriptor.disabled(
        stream="test",
        schema={"type": "object"},
    )
    expected = {
        "stream": "test",
        "tap_stream_id": "test",
        "schema": {"type": "object"},
        "metadata": [
            {
                "metadata": {
                    "selected": False,
                },
                "breadcrumb": [],
            },
        ],
    }
    assert descriptor.dict() == expected
