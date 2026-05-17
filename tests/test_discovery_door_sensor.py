from assertpy import assert_that


def test_door_sensor_model_discovery_payload_device_data():
    from discovery_handlers.door_sensor_discovery import DoorSensorDiscovery

    discovery = DoorSensorDiscovery("TestSensor", "1234", "GS-WDS07")
    payload = discovery.getDiscoveryPayload("rtl_433/TestSensor")
    assert_that(payload).contains_key("dev")
    assert_that(payload["dev"]).contains_key("ids")
    assert_that(payload["dev"]["ids"]).is_equal_to("1234")
    assert_that(payload["dev"]).contains_key("name")
    assert_that(payload["dev"]["name"]).is_equal_to("TESTSENSOR Door Sensor")
    assert_that(payload["dev"]).contains_key("mdl")
    assert_that(payload["dev"]["mdl"]).is_equal_to("GS-WDS07")
    assert_that(payload["dev"]).contains_key("sw")
    assert_that(payload["dev"]["sw"]).is_equal_to("GS-WDS07")


def test_door_sensor_generic_remote_discovery_payload_device_data():
    from discovery_handlers.door_sensor_discovery import DoorSensorDiscovery

    discovery = DoorSensorDiscovery("TestSensor", "1234", "Generic-Remote")
    payload = discovery.getDiscoveryPayload("rtl_433/TestSensor")
    assert_that(payload).contains_key("cmps")
    assert_that(payload["cmps"]).contains_key("doorStatus")
    assert_that(payload["cmps"]["doorStatus"]).contains_key("value_template")
    assert_that(payload["cmps"]["doorStatus"]["value_template"]).is_equal_to(
        "{{ value_json.cmd | int }}"
    )
    assert_that(payload["cmps"]["doorStatus"]).contains_key("payload_on")
    assert_that(payload["cmps"]["doorStatus"]["payload_on"]).is_equal_to(10)
    assert_that(payload["cmps"]["doorStatus"]).contains_key("payload_off")
    assert_that(payload["cmps"]["doorStatus"]["payload_off"]).is_equal_to(14)
    assert_that(payload["cmps"]["doorStatus"]).contains_key("state_topic")
    assert_that(payload["cmps"]["doorStatus"]["state_topic"]).is_equal_to(
        "rtl_433/TestSensor/state/door"
    )
