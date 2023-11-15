from typing import List

class SensorMapping:
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

    @classmethod
    def from_dict(cls, data: dict) -> 'SensorMapping':
        return cls(**data)

class Config:
    def __init__(self, DTE_IP: str, RTL_IP: str, sensorMappings: List[SensorMapping]) -> None:
        self.DTE_IP = DTE_IP
        self.RTL_IP = RTL_IP
        self.sensorMappings = sensorMappings

    @classmethod
    def from_dict(cls, data: dict) -> 'Config':
        sensorMappings = [SensorMapping.from_dict(sm) for sm in data['sensorMappings']]
        return cls(data['DTE_IP'], data['RTL_IP'], sensorMappings)