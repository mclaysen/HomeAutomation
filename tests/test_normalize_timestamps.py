# trunk-ignore-all(bandit/B101)

from datetime import datetime
from utilities import normalize_timestamp

def test_adds_default_timezone_for_naive_timestamp():
    result = normalize_timestamp("2026-01-15 10:30:00")
    dt = datetime.fromisoformat(result)

    assert dt.tzinfo is not None
    assert result == "2026-01-15T10:30:00-05:00"

def test_keeps_existing_timezone():
    result = normalize_timestamp("2026-01-15T10:30:00+00:00")
    assert result == "2026-01-15T10:30:00+00:00"

def test_normalizes_space_separator():
    result = normalize_timestamp("2026-04-13 09:15:00")
    assert "T" in result