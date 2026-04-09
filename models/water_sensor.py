class WaterSensorData:
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


    @classmethod
    def from_dict(cls, data: dict) -> 'WaterSensorData':
        return cls(**data)