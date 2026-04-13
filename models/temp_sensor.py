from datetime import datetime
from zoneinfo import ZoneInfo

def normalize_timestamp(timestamp: str) -> str:
    #todo: make this generic
    raw = timestamp.replace(" ", "T")
    dt = datetime.fromisoformat(raw)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("America/New_York"))
    return dt.isoformat()


class TempSensorData:
    def __init__(self, time: str, model: str, id: int, channel: str, battery_ok: int, temperature_C: float, humidity: int, mic: str) -> None:
        self.time = time
        self.model = model
        self.id = id
        self.channel = channel
        self.battery_ok = battery_ok
        self.temperature_C = temperature_C
        self.humidity = humidity
        self.mic = mic

    @classmethod
    def from_dict(cls, data: dict) -> 'TempSensorData':
        normlized = dict(data)
        if "time" in normlized:
            normlized["time"] = normalize_timestamp(normlized["time"])
        return cls(**normlized)