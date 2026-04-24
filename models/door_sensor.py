class DoorSensorData:
    def __init__(self, time: str, model: str, id: int, cmd: int, tristate: str) -> None:
        self.time = time
        self.model = model
        self.house_code = id
        self.command = cmd
        self.tri_state = tristate

    @classmethod
    def from_dict(cls, data: dict) -> 'DoorSensorData':
        # Convert keys with spaces to keys with underscores
        data = {key.replace(' ', '_'): value for key, value in data.items()}
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'model': self.model,
            'id': self.house_code,
            'cmd': self.command,
            'tristate': self.tri_state
        }