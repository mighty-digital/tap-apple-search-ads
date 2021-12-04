from tap_apple_search_ads.stream.api import Descriptor, Metadata
from tap_apple_search_ads.stream.concrete.base import ConcreteStreamBase


def test_set_descriptor():
    stream = ConcreteStreamBase("test", "test", {})
    assert stream.descriptor() == Descriptor("test", "test", {}, [Metadata.disabled()])
    new_descriptor = Descriptor(
        "test_", "test_", {"type": "object"}, [Metadata(True, ("properties",))]
    )
    stream.set_descriptor(new_descriptor)
    assert stream.descriptor() == new_descriptor


def test_unset_descriptor():
    stream = ConcreteStreamBase("test", "test", {})
    new_descriptor = Descriptor(
        "test_", "test_", {"type": "object"}, [Metadata(True, ("properties",))]
    )
    stream.set_descriptor(new_descriptor)
    assert stream.descriptor() == new_descriptor
    stream.set_descriptor(None)
    assert stream.descriptor() == Descriptor("test", "test", {}, [Metadata.disabled()])
