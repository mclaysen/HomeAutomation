import json

from assertpy import assert_that

from models.leak_sensor import LeakSensor, LeakSensorEvent
from models.sensor_mappings import Config, ModelMapping, SensorMapping
from models.sensor_types import SensorType
from mqtt_handlers.message_handlers.leak_sensor_handler import LeakSensorHandler
from mqtt_handlers.subscriber_model import SubscriberModel
from tests.fake_logger import FakeLogger
from tests.fake_mqttsubscriber import FakeMqttPublisher


def test_leak_sensor_handler_publishes_read_received_timestamp():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)
    config = Config(
        DTE_IP="127.0.0.1",
        RTL_IP="127.0.0.1",
        HOME_ASSISTANT_IP="127.0.0.1",
        ModelMappings=[
            ModelMapping(
                model="Govee-Water",
                sensorType=SensorType.LEAK_SENSOR,
                sensors=[SensorMapping(name="kitchen_sink", id=7347)],
            )
        ],
    )
    subscriber_data = SubscriberModel(
        deviceType="rtl_433", topic="rtl_433/#", ip="127.0.0.1", port=1883
    )
    handler = LeakSensorHandler(subscriber_data, config, publisher, logger)
    payload = LeakSensor(
        time="2026-09-02T22:48:25-04:00",
        model="Govee-Water",
        id=7347,
        event=LeakSensorEvent.WATER_LEAK,
        code="0x01",
        mic="CRC",
        detect_wet=1,
    )

    handler.on_message(payload)

    topic, message, qos, retain = publisher.published_messages[0]
    assert_that(topic).is_equal_to("rtl_433/leak_sensor/kitchen_sink")
    assert_that(json.loads(message)).is_equal_to({"time": "2026-09-02T22:48:25-04:00"})
    assert_that(qos).is_equal_to(0)
    assert_that(retain).is_false()
