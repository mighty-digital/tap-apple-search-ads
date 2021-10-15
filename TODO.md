# TODO

## Implement multiple stream discovery based on selectors passed in config

Given config `sample-config.json`

In do_discover generate as many campaign_level_report streams as properties in config#campaign_level_reports#selectors with names campaign_level_reports__{selector_name}
Reuse the same (non-flat) schema for each of them.

Try doing testing using pytest.
