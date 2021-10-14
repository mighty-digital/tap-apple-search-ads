# Apple Search Ads Singer Tap

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
