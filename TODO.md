# TODO

## Implement start_time and end_time reading from config

Change default selector to exclude start_time and end_time.
Look for start_time in config.json - if missing - fail.
Look for end_time in config.json - if missing - use today.

All dates should be parsed with UTC timezone (datetime.timezone.utc).
Create API_DATE_FORMAT strign constant to use with datetime.strftime.
