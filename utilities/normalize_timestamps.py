# generate an exportable function that can normalize timestamps in a given dataset
from datetime import datetime
from zoneinfo import ZoneInfo

def normalize_timestamp(timestamp: str, timezone: str = "America/New_York") -> str:

    raw = timestamp.replace(" ", "T")
    dt = datetime.fromisoformat(raw)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(timezone))
    return dt.isoformat()