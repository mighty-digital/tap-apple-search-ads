# Apple Search Ads Singer Tap

[Singer.io](https://www.singer.io/) Tap for [Apple Search Ads](https://searchads.apple.com/) API.

## Features

* Covers 2 endpoints - **Campaign** and **Campaign Level Reports**.
* Available streams offer formatting variations of objects from given endpoints - unstructured objects, flat objects.
* Supports [discovery mode](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode) and generates a proper Singer catalog.
* Streams that provide "flat" objects can be used directly with SQL database targets, such as [target-csv](https://github.com/singer-io/target-csv) or [pipelinewise-target-postgres](https://github.com/transferwise/pipelinewise-target-postgres).
* Streams that provide "raw" objects can be used with unstructured targets, such as [target-json](https://github.com/dvelardez/target-json).

## Installation

Ensure that [Python](https://www.python.org/downloads/) is installed. Minimun required version is Python 3.8.

Tap is currently not available on [PyPI](https://pypi.org/), so direct `pip install tap-apple-search-ads` is not possible. Install the Tap [from a local src tree](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-a-local-src-tree).

```pwsh
# Example of global installation on Windows.
PS C:\tap-apple-search-ads-tutorial>
git clone https://github.com/mighty-digital/tap-apple-search-ads
PS C:\tap-apple-search-ads-tutorial>
pip install './tap-apple-search-ads'
PS C:\tap-apple-search-ads-tutorial>
tap-apple-search-ads.exe --config .\config.json --discover > catalog.json
```

```pwsh
# Example of venv installation on Windows.
PS C:\tap-apple-search-ads-tutorial>
git clone https://github.com/mighty-digital/tap-apple-search-ads
PS C:\tap-apple-search-ads-tutorial>
python.exe -m venv .envs/tap
PS C:\tap-apple-search-ads-tutorial>
.\.envs\tap\Scripts\Activate.ps1
PS C:\tap-apple-search-ads-tutorial>
(tap) pip install './tap-apple-search-ads'
PS C:\tap-apple-search-ads-tutorial>
(tap) tap-apple-search-ads.exe --config .\config.json --discover > catalog.json
```

## Configuration

Required `config.json` values:

- `client_id: string`
- `key_id: string`
- `team_id: string`
- `org_id: string or integer`
- `private_key_value: string` - literal private key value as string (joined with `\n` character); or `private_key_file: string` - path to file with private key value

Obtain all of the values by following [Implementing OAuth for the Apple Search Ads API](https://developer.apple.com/documentation/apple_search_ads/implementing_oauth_for_the_apple_search_ads_api) guide up to and including "Upload a Public Key" step. "Create a Client Secret" step and the following steps are implemented in the Tap itself.

## Development

### pre-commit

This project uses [pre-commit](pre-commit.com). Run `pre-commit install` to install pre-commit into your git hooks. pre-commit will now run on every commit. Running `pre-commit install` should always be the first thing you do.
