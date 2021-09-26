import datetime


def now() -> float:
    return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
