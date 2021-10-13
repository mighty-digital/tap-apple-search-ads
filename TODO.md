# Implementing campaign_level_reports stream

Apple Search Ads docs - https://developer.apple.com/documentation/apple_search_ads/get_campaign-level_reports

## Create object json-schema

Create flat schema from

* https://developer.apple.com/documentation/apple_search_ads/row
* https://developer.apple.com/documentation/apple_search_ads/extendedspendrow

How to:

1. Create 2 separate schemas - row.json, extendedspendrow.json
2. Create merged campaign_level_reports schema

## Add campaign_level_reports stream sync

POST https://api.searchads.apple.com/api/v4/reports/campaigns

Add file src/tap_apple_search_ads/campaign_level_reports.py

Use predefined Selector (anything that works). Event start_date end_date can be statically defined.
Also can read start_date from config and set end_date as datetime.now().

Add new statement to __init__.py#sync_concrete_stream.

## Definition of Done

```bash
> python -m tap_apple_search_ads --config config.json --discover > catalog.json
> python -m tap_apple_search_ads --config config.json --catalog catalog.json
```

stdout should have records for 2 streams:
campaign
campaign_level_reports
