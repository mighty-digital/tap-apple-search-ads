# Apple Search Ads Singer Tap

[Singer.io](https://www.singer.io/) Tap for [Apple Search Ads](https://searchads.apple.com/) API.

## Features

- Covers 2 endpoints - **Campaign** and **Campaign Level Reports**.
- Available streams offer formatting variations of objects from given endpoints - unstructured objects, flat objects.
- Supports [discovery mode](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode) and generates a proper Singer catalog.
- Streams that provide "flat" objects can be used directly with SQL database targets, such as [target-csv](https://github.com/singer-io/target-csv) or [pipelinewise-target-postgres](https://github.com/transferwise/pipelinewise-target-postgres).
- Streams that provide "raw" objects can be used with unstructured targets, such as [target-json](https://github.com/dvelardez/target-json).

## Installation

Ensure that [Python](https://www.python.org/downloads/) is installed. The minimum required version is Python 3.8.

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

## Usage

To use the Tap, you need to create the `config.json` file with the values required to access the [Apple Search Ads API](https://developer.apple.com/documentation/apple_search_ads).

### Creating the config.json file

To access the Search Ads API you need to create a Public and Private Key pair and upload the Public Key to the Search Ads UI.

If you already have the Public Key uploaded, use the `clientId, teamId, keyId` values associated with the existing key.

If not, follow the steps outlined in [Implementing OAuth for the Apple Search Ads API](https://developer.apple.com/documentation/apple_search_ads/implementing_oauth_for_the_apple_search_ads_api). Complete the "Invite Users", "Generate a Private Key", "Extract a Public Key", "Upload a Public Key" steps to obtain the `clientId, teamId, keyId` values.

To generate the Private and Public Key pair you need to have the `openssl` program installed and configured to complete the steps. `openssl` program is usually already installed in most Linux distributions by default. In Windows, you can either use the `openssl` program provided with [Git for Windows](https://gitforwindows.org/) or [Miniconda/Anaconda](https://docs.conda.io/en/latest/miniconda.html) (or similar) or get the binary from the [OpenSSL](https://wiki.openssl.org/index.php/Binaries).

`config.json` values required for Apple Search Ads API:

- `org_id: string or integer` - Apple Search Ads Organization ID, obtained from Apple Search Ads console.
- `client_id: string` - obtained from "Implementing OAuth for the Apple Search Ads API".
- `key_id: string` - obtained from "Implementing OAuth for the Apple Search Ads API".
- `team_id: string` - obtained from "Implementing OAuth for the Apple Search Ads API".
- `private_key_file: string` - path to the `private-key.pem` file obtained from "Implementing OAuth for the Apple Search Ads API".
- `private_key_value: string` - contents of the `private-key.pem` file as string (joined with `\n` character).

You only need one of the private key values (`private_key_file` or `private_key_value`) in the `config.json` file.

After creating the `config.json` file and filling it with the relevant values, proceed to the **Discovery** step.

### Discovery

The first step of the actual Tap usage is the Discovery:

```pwsh.exe
tap-apple-search-ads.exe --config .\config.json --discover > catalog.json
```

This command will create the `catalog.json` file in the current working directory. This file contains descriptions of the available streams and their metadata. By default, every stream metadata consists only of the selection marker, and every stream is NOT selected by default. You need to alter the default `catalog.json` to enable the stream for syncing. Locate the relevant stream object in the `catalog.json`, then locate the `metadata` array inside the stream object, then locate the object with `"breadcrumb": []` and set the `"selected"` value of the object to `true`.

Currently, per-field metadata is not used, only whole streams can be enabled or disabled.

After creating the `catalog.json` file and selecting desired streams in the file, proceed to the **Sync** step.

### Sync

Running the Tap with the `--catalog` option will enable the Sync mode.

```pwsh
tap-apple-search-ads.exe --config .\config.json --catalog .\catalog.json
```

This command will output the Singer messages to the STDOUT. The output of the command can be piped directly into the Singer Targets.

### Usage Example.

In this example you will learn to run the `tap-apple-search-ads`, starting with installation and ending with the "campaign_flat" stream sync.

#### Installation

```pwsh
PS C:\tap-apple-search-ads-tutorial>
git clone https://github.com/mighty-digital/tap-apple-search-ads
PS C:\tap-apple-search-ads-tutorial>
python.exe -m venv .envs/tap
PS C:\tap-apple-search-ads-tutorial>
.\.envs\tap\Scripts\Activate.ps1
PS C:\tap-apple-search-ads-tutorial>
(tap) pip install './tap-apple-search-ads'
```

#### Creation of the config.json

Ensure that `private-key.pem` file is created and located in the `C:\tap-apple-search-ads-tutorial` directory.

```pwsh
PS C:\tap-apple-search-ads-tutorial>
Write-Output '{
>>   "client_id": "<your clientId>",
>>   "team_id": "<your teamId>",
>>   "key_id": "<your keyId>",
>>   "org_id": "<your orgId>",
>>   "private_key_value": "C:/tap-apple-search-ads-tutorial/private-key.pem"
>> }' | Out-File config.json
```

#### Discovery

```pwsh
# Obtain the catalog.json
PS C:\tap-apple-search-ads-tutorial>
(tap) tap-apple-search-ads.exe --config .\config.json --discover > catalog.json
# Edit the catalog.json
PS C:\tap-apple-search-ads-tutorial>
(tap) nvim.exe catalog.json
# Locate the "stream": "campaign_flat" object:
{
  "stream": "campaign_flat",
  "tap_stream_id": "campaign_flat",
  "schema": {
    ...
  },
  "metadata": [
    {
      "metadata": {
        "selected": false
      },
      "breadcrumb": []
    }
  ]
}
# Set the "selected" field to true
{
  "stream": "campaign_flat",
  "tap_stream_id": "campaign_flat",
  "schema": {
    ...
  },
  "metadata": [
    {
      "metadata": {
        "selected": true
      },
      "breadcrumb": []
    }
  ]
}
# Save the file
```

#### Sync

We will use the `target-csv` package as a Singer Target. This package requires a different version of the `singer-python`, so it will be installed into the different `venv`.

```pwsh
PS C:\tap-apple-search-ads-tutorial>
(tap) deactivate
PS C:\tap-apple-search-ads-tutorial>
python.exe -m venv .envs/target
PS C:\tap-apple-search-ads-tutorial>
.\.envs\target\Scripts\Activate.ps1
PS C:\tap-apple-search-ads-tutorial>
(target) pip install target-csv
PS C:\tap-apple-search-ads-tutorial>
(target) deactivate
PS C:\tap-apple-search-ads-tutorial>
.\.envs\tap\Scripts\tap-apple-search-ads.exe --config .\config.json --catalog .\catalog.json | .\.envs\target\Scripts\target-csv.exe
PS C:\tap-apple-search-ads-tutorial>
cat .\campaign_flat-20220629T154605.csv
```

If you have any campaigns in your Apple Search Ads Organization, their data will be stored in the generated `.csv` file.

## Development

To work on the Tap development, install additional dependencies from the `setup.cfg` file. Possible contributions:

- Adding additional API Endpoints and corresponding Streams.
- Adding more Singer metadata - per-field metadata parsing and usage.

### Installation for development

```pwsh
PS C:\tap-apple-search-ads-tutorial>
git clone https://github.com/mighty-digital/tap-apple-search-ads
PS C:\tap-apple-search-ads-tutorial>
python.exe -m venv .envs/tap
PS C:\tap-apple-search-ads-tutorial>
.\.envs\tap\Scripts\Activate.ps1
PS C:\tap-apple-search-ads-tutorial>
(tap) pip install './tap-apple-search-ads[dev,test]'
```

### pre-commit

This project uses [pre-commit](pre-commit.com). Run `pre-commit install` to install pre-commit into your git hooks. pre-commit will now run on every commit. Running `pre-commit install` should always be the first thing you do.
