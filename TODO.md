# Implement flat schema for campaing stream and add it as a campaign_flat stream

## Modify schema to remove objects and arrays from properties

Replace Money properties with `__currency` and `__amount` properties.
Repalce properties with types `object` and `array` with `"type": "string"`.

## Implement transformation in tap code

Complete `tap_apple_search_ads/api/campaign.py#to_flat_schema` fuction:

* Unwrap Money objects - split into `__currency` and `__amount`.
* JSON serialize other objects and arrays

## Add new stream and schema to dicsovery mode

Add new stream name to `STREAMS` constant.

## Add new stream to sync mode

Add new case to `sync_concrete_stream` - same as `campaign` but with `to_flat_schema` applied to all records.
