from typing import List

class SensorMapping:
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

    @classmethod
    def from_dict(cls, data: dict) -> 'SensorMapping':
        return cls(**data)

class ModelMapping:
    def __init__(self, model: str, sensors: List[SensorMapping]) -> None:
        self.model = model
        self.sensors = sensors

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelMapping':
        sensors = [SensorMapping.from_dict(sm) for sm in data['Sensors']]
        return cls(data['Model'], sensors)
class Config:
    def __init__(self, DTE_IP: str, RTL_IP: str, HOME_ASSISTANT_IP: str, ModelMappings: List[ModelMapping]) -> None:
        self.DTE_IP = DTE_IP
        self.RTL_IP = RTL_IP
        self.HOMEASSISTANT_IP = HOME_ASSISTANT_IP
        self.ModelMappings = ModelMappings

    @classmethod
    def from_dict(cls, data: dict) -> 'Config':
        modelMappings = [ModelMapping.from_dict(sm) for sm in data['ModelMappings']]
        return cls(data['DTE_IP'], data['RTL_IP'], data['HOME_ASSISTANT_IP'], modelMappings)