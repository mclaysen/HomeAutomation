from assertpy import assert_that
from models.temp_sensor import TempSensor
from mqtt_handlers.subscriber_model import SubscriberModel
from tests.fake_mqttsubscriber import FakeMqttPublisher
from mqtt_handlers.message_handlers.rtl_message_handler import RtlMessageHandler
from models.sensor_mappings import Config, SensorMapping, ModelMapping
from tests.fake_logger import FakeLogger

def test_rtl_message_handler_init():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)

    model_mapping = [ModelMapping(model="test_model", sensorType = "TEMP_SENSOR", sensors=[SensorMapping(name="test_sensor", id=1)])]

    subsciberData = SubscriberModel(deviceType="rtl_433", topic="rtl_433/#", ip="127.0.0.1", port=1883)
    configTest = Config(DTE_IP="127.0.0.1", RTL_IP="127.0.0.1", HOME_ASSISTANT_IP="127.0.0.1", ModelMappings=model_mapping)
    handler = RtlMessageHandler(subsciberData, configTest, publisher, logger)

    payload = TempSensor(time="2025-01-01T00:00:00Z", model="test_model", id=1, channel="A", battery_ok=1, temperature_C=25.0, humidity=50.0, mic="CRC")

    handler.on_message(payload)

    expected_message: tuple[str, str, int, bool] = (
        "rtl_433/test_sensor",
        '{"time": "2025-01-01T00:00:00+00:00", "model": "test_model", "id": 1, "channel": "A", "battery_ok": 1, "temperature_C": 25.0, "humidity": 50.0, "mic": "CRC"}',
        0,
        False,
        )
    assert_that(publisher.published_messages.pop()).is_equal_to(expected_message)

