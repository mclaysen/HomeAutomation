from datetime import datetime
from zoneinfo import ZoneInfo

def normalize_timestamp(timestamp: str, timezone: str = "America/New_York") -> str | None:
    try:
        raw = timestamp.replace(" ", "T")
        dt = datetime.fromisoformat(raw)
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {timestamp}") from e

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(timezone))
    return dt.isoformat()