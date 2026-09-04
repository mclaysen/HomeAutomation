import json

from assertpy import assert_that

from discovery_handlers.publish_discovery import publish_discovery
from models.sensor_mappings import Config, ModelMapping, SensorMapping
from models.sensor_types import SensorType
from tests.fake_discovery import FakeDiscoveryFactory
from tests.fake_logger import FakeLogger
from tests.fake_mqttsubscriber import FakeMqttPublisher


def _make_config(mappings: list[ModelMapping]) -> Config:
    return Config(
        DTE_IP="127.0.0.1",
        RTL_IP="127.0.0.1",
        HOME_ASSISTANT_IP="127.0.0.1",
        ModelMappings=mappings,
    )


def test_publish_discovery_temp_sensor_calls_factory_and_publishes():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)
    factory = FakeDiscoveryFactory()

    config = _make_config(
        [
            ModelMapping(
                model="Acurite-Tower",
                sensorType=SensorType.TEMP_SENSOR,
                sensors=[SensorMapping(name="backyard", id=101)],
            )
        ]
    )

    publish_discovery(publisher, config, factory)

    assert_that(factory.calls).is_length(1)
    assert_that(factory.calls[0]).is_equal_to(
        (SensorType.TEMP_SENSOR, "backyard", "101", None)
    )

    assert_that(publisher.published_messages).is_length(1)
    topic, payload, qos, retain = publisher.published_messages[0]
    assert_that(topic).is_equal_to("homeassistant/device/backyard/101/config")
    assert_that(json.loads(payload)["state_topic"]).is_equal_to("rtl_433/backyard")
    assert_that(qos).is_equal_to(1)
    assert_that(retain).is_true()


def test_publish_discovery_door_sensor_passes_model_to_factory():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)
    factory = FakeDiscoveryFactory()

    config = _make_config(
        [
            ModelMapping(
                model="Honeywell-Series",
                sensorType=SensorType.DOOR_SENSOR,
                sensors=[SensorMapping(name="front_door", id=202)],
            )
        ]
    )

    publish_discovery(publisher, config, factory)

    assert_that(factory.calls[0]).is_equal_to(
        (SensorType.DOOR_SENSOR, "front_door", "202", "Honeywell-Series")
    )


def test_publish_discovery_multiple_sensors_publishes_once_per_sensor():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)
    factory = FakeDiscoveryFactory()

    config = _make_config(
        [
            ModelMapping(
                model="Acurite-Tower",
                sensorType=SensorType.TEMP_SENSOR,
                sensors=[
                    SensorMapping(name="backyard", id=101),
                    SensorMapping(name="garage", id=102),
                ],
            )
        ]
    )

    publish_discovery(publisher, config, factory)

    assert_that(factory.calls).is_length(2)
    assert_that(publisher.published_messages).is_length(2)


def test_publish_discovery_skips_unknown_sensor_type():
    logger = FakeLogger()
    publisher = FakeMqttPublisher(logger)
    factory = FakeDiscoveryFactory()

    config = _make_config(
        [
            ModelMapping(
                model="unknown",
                sensorType=0,
                sensors=[SensorMapping(name="basement", id=303)],
            )
        ]
    )

    publish_discovery(publisher, config, factory)

    assert_that(factory.calls).is_empty()
    assert_that(publisher.published_messages).is_empty()
