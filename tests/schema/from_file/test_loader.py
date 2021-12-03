from pathlib import Path

import pytest

from tap_apple_search_ads.schema.from_file import api

TESTDATA = Path(__file__).absolute() / "testdata"
BASIC = TESTDATA / "basic"


def test_loader_init():
    loader = api.Loader(BASIC)

    assert loader.path == BASIC
    assert loader.schemas == {}


def test_loader_init_str():
    loader = api.Loader(BASIC.absolute().as_posix())

    assert loader.path == BASIC
    assert loader.schemas == {}


@pytest.mark.skip(reason="not implemented")
def test_loader_basic():
    schemas_directory = TESTDATA / "basic"

    loader = api.Loader(schemas_directory)

    expected = {"type": "object"}
    for name in list("abc"):
        schema = loader.get_schema_by_name(name)
        assert expected == schema
