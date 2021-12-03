from pathlib import Path

import pytest

from tap_apple_search_ads.schema.from_file import api

TESTDATA = Path(__file__).parent.absolute() / "testdata"
BASIC = TESTDATA / "basic"


def test_loader_init():
    loader = api.Loader(BASIC)

    assert loader.path == BASIC
    assert loader.schemas == {}


def test_loader_init_str():
    loader = api.Loader(BASIC.absolute().as_posix())

    assert loader.path == BASIC
    assert loader.schemas == {}


def test_loader_fails_on_missing_dir():
    loader = api.Loader(TESTDATA / "missing")

    with pytest.raises(api.LoaderError):
        loader.get_schema_by_name("a.json")


def test_loader_fails_on_non_dir():
    loader = api.Loader(BASIC / "a.json")

    with pytest.raises(api.LoaderError):
        loader.get_schema_by_name("a.json")


def test_loader_schema_import():
    loader = api.Loader(BASIC)

    loader.get_schema_by_name("a.json")

    assert loader.schemas


def test_loader_fails_on_non_json_dir():
    loader = api.Loader(TESTDATA / "non-json")

    with pytest.raises(api.LoaderError):
        loader.get_schema_by_name("a.json")


def test_loader_basic():
    schemas_directory = TESTDATA / "basic"

    loader = api.Loader(schemas_directory)

    expected = {"type": "object"}
    for name in list("abc"):
        schema = loader.get_schema_by_name(name + ".json")
        assert schema == expected
