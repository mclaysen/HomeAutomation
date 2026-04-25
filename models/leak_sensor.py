from utilities import normalize_timestamp

class LeakSensor:
    def __init__(self, time: str, model: str, id: int, event: str, code: str, mic: str, detect_wet: bool | None = None, battery_ok: float | None = None, battery_mV: int | None = None, leak_num: int | None = None) -> None:
        self.time = time
        self.model = model
        self.id = id
        self.event = event
        self.code = code
        self.mic = mic
        self.detect_wet = detect_wet
        self.battery_ok = battery_ok
        self.battery_mV = battery_mV
        self.leak_num = leak_num

    @property
    def time(self) -> str:
        return self._time

    @time.setter
    def time(self, value: str) -> None:
        self._time = normalize_timestamp(value)

    @classmethod
    def from_dict(cls, data: dict) -> 'LeakSensor':
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'model': self.model,
            'id': self.id,
            'event': self.event,
            'code': self.code,
            'mic': self.mic,
            'detect_wet': self.detect_wet,
            'battery_ok': self.battery_ok,
            'battery_mV': self.battery_mV,
            'leak_num': self.leak_num
        }