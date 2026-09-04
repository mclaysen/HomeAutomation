from discovery_handlers.abstract_discovery_handler import AbstractDiscoveryHandler
from discovery_handlers.discovery_factory import DiscoveryFactory
from models.sensor_types import SensorType


class FakeDiscoveryHandler(AbstractDiscoveryHandler):
    def getDiscoveryPayload(self, stateTopic: str) -> dict:
        return {"state_topic": stateTopic, "name": self.sensorName}


class FakeDiscoveryFactory(DiscoveryFactory):
    def __init__(self):
        self.calls: list[tuple] = []

    def get_discovery_object(
        self,
        sensorType: SensorType,
        sensorName: str,
        sensorId: str,
        sensorModel: str | None,
    ) -> AbstractDiscoveryHandler:
        self.calls.append((sensorType, sensorName, sensorId, sensorModel))
        return FakeDiscoveryHandler(sensorType, sensorName, sensorId, sensorModel)
