from utilities.normalize_timestamps import normalize_timestamp

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

    @property
    def time(self) -> str:
        return self._time

    @time.setter
    def time(self, value: str) -> None:
        self._time = normalize_timestamp(value)

    @classmethod
    def from_dict(cls, data: dict) -> 'TempSensorData':
        return cls(**data)