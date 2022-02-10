from datetime import datetime, timezone


def now() -> str:
    now = datetime.now(tz=timezone.utc)
    return now.isoformat()