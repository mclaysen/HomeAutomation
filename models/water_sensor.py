class WaterSensorData:
    def __init__(self, time: str, model: str, id: int, event: str, detect_wet: bool, code: str, mic: str) -> None:
        self.time = time
        self.model = model
        self.id = id
        self.event = event
        self.detect_wet = detect_wet
        self.code = code
        self.mic = mic

    @classmethod
    def from_dict(cls, data: dict) -> 'WaterSensorData':
        return cls(**data)