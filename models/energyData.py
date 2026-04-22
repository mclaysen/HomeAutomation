from models.energyType import EnergyType

class EnergyData:
    def __init__(self, type: EnergyType, time: int, value: float) -> None:
        self.type = type
        self.time = time
        self.value = value

    @classmethod
    def from_dict(cls, data: dict):
        energyType = EnergyType.MINUTE
        if not data.get('type'):
            energyType = EnergyType.INSTANT
        value = 0.0
        if energyType == EnergyType.INSTANT:
            value = data['demand']
        else:
            value = data['value']
        return cls(energyType, data['time'], value)

    def to_dict(self):
        return {
            'type': self.type.value,
            'time': self.time,
            'value': self.value
        }
