from enum import Enum
import logging
from models.battery_level import BatteryLevel

from utilities import normalize_timestamp

class LeakSensorEvent(Enum):
    BUTTON_PRESS = 'Button Press'
    WATER_LEAK = 'Water Leak'
    BATTERY_REPORT = 'Battery Report'
    UNKNOWN = 'Unknown'
    INVALID = 'Invalid'

class LeakSensor:
    def __init__(self, time: str, model: str, id: int, event: str | LeakSensorEvent, code: str, mic: str, detect_wet: int | None = None, battery_ok: float | None = None, battery_mV: int | None = None, leak_num: int | None = None) -> None:
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
        try:
            self._time = normalize_timestamp(value)
        except ValueError as value_error:
            logging.error("Error normalizing timestamp: %s", value_error)
            raise ValueError(f"Invalid timestamp format: {value}") from value_error
    @property
    def event(self) -> LeakSensorEvent:
        return self._event

    @event.setter
    def event(self, value: str | LeakSensorEvent) -> None:
        try:
            if isinstance(value, str):
                self._event = LeakSensorEvent(value)
            elif isinstance(value, LeakSensorEvent):
                self._event = value
            else:
                logging.error("Invalid type for event: %s. Expected str or LeakSensorEvent.", type(value))
                self._event = LeakSensorEvent.INVALID
        except ValueError:
            logging.error("Unknown event type: %s", value)
            self._event = LeakSensorEvent.INVALID

    @property
    def battery_level(self) -> BatteryLevel:
        if self.battery_ok is not None:
            if self.battery_ok >= 0.26:
                return BatteryLevel.OK
            elif self.battery_ok > 0.24:
                return BatteryLevel.LOW
            else:
                return BatteryLevel.EMPTY
        return BatteryLevel.UNKNOWN

    @property
    def detect_wet(self) -> bool | None:
        return self._detect_wet

    @detect_wet.setter
    def detect_wet(self, value: int | None) -> None:
        if value is not None:
            if value == 1:
                self._detect_wet = True
            elif value == 0:
                self._detect_wet = False
            else:
                logging.error("Invalid value for detect_wet: %s. Expected 0 or 1.", value)
                self._detect_wet = None
        else:
            self._detect_wet = None

    @classmethod
    def from_dict(cls, data: dict) -> 'LeakSensor':
        required_fields = ('time', 'model', 'id', 'code', 'mic')
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            message = f"Missing required field(s): {', '.join(missing_fields)}"
            logging.error("%s in data: %s", message, data)
            raise ValueError(message)

        time_value = data['time']
        model_value = data['model']
        id_value = data['id']
        code_value = data['code']
        mic_value = data['mic']

        if not isinstance(time_value, str) or not time_value.strip():
            raise ValueError("Field 'time' must be a non-empty string")
        if not isinstance(model_value, str) or not model_value.strip():
            raise ValueError("Field 'model' must be a non-empty string")
        if not isinstance(id_value, int):
            raise ValueError("Field 'id' must be an int")
        if not isinstance(code_value, str) or not code_value.strip():
            raise ValueError("Field 'code' must be a non-empty string")
        if not isinstance(mic_value, str) or not mic_value.strip():
            raise ValueError("Field 'mic' must be a non-empty string")

        return cls(
            time=time_value,
            model=model_value,
            id=id_value,
            event=data.get('event', LeakSensorEvent.UNKNOWN),
            code=code_value,
            mic=mic_value,
            detect_wet=data.get('detect_wet'),
            battery_ok=data.get('battery_ok'),
            battery_mV=data.get('battery_mV'),
            leak_num=data.get('leak_num')
    )

    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'model': self.model,
            'id': self.id,
            'event': self.event.value,
            'code': self.code,
            'mic': self.mic,
            'detect_wet': self.detect_wet,
            'battery_ok': self.battery_ok,
            'battery_mV': self.battery_mV,
            'leak_num': self.leak_num,
            'battery_level': self.battery_level.value
        }