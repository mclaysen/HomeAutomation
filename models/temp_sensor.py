from typing import Optional

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
        return cls(**data)