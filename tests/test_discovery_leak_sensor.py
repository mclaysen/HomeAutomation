from assertpy import assert_that

from discovery_handlers.leak_sensor_discovery import LeakSensorDiscovery


def test_leak_sensor_model_discovery_payload_device_data():
    discovery = LeakSensorDiscovery("TestSensor", "1234")
    payload = discovery.getDiscoveryPayload("rtl_433/TestSensor")
    assert_that(payload).contains_key("dev")
    assert_that(payload["dev"]).contains_key("ids")
    assert_that(payload["dev"]["ids"]).is_equal_to("1234")
    assert_that(payload["dev"]).contains_key("name")
    assert_that(payload["dev"]["name"]).is_equal_to("TESTSENSOR Leak Sensor")
    assert_that(payload["dev"]).contains_key("mdl")
    assert_that(payload["dev"]["mdl"]).is_equal_to("H5054")


def test_leak_sensor_generic_remote_discovery_payload_device_data():
    discovery = LeakSensorDiscovery("TestSensor", "1234")
    payload = discovery.getDiscoveryPayload("rtl_433/TestSensor")
    assert_that(payload).contains_key("cmps")
    assert_that(payload["cmps"]).contains_key("leakStatus")
    assert_that(payload["cmps"]["leakStatus"]).contains_key("value_template")
    assert_that(payload["cmps"]["leakStatus"]["value_template"]).is_equal_to(
        "{{ value_json.water_ok | int }}"
    )
    assert_that(payload["cmps"]["leakStatus"]).contains_key("payload_on")
    assert_that(payload["cmps"]["leakStatus"]["payload_on"]).is_equal_to(0)
    assert_that(payload["cmps"]["leakStatus"]).contains_key("payload_off")
    assert_that(payload["cmps"]["leakStatus"]["payload_off"]).is_equal_to(1)
    assert_that(payload["cmps"]["leakStatus"]).contains_key("state_topic")
    assert_that(payload["cmps"]["leakStatus"]["state_topic"]).is_equal_to(
        "rtl_433/TestSensor/state/leak"
    )
