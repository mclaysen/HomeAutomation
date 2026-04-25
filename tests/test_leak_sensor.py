from assertpy import assert_that
from pytest import mark
from models.battery_level import BatteryLevel
from models.leak_sensor import LeakSensor, LeakSensorEvent

@mark.parametrize("data, expected_detect_wet", [(0, False), (1, True), (-1, None), (None, None)])
def test_leak_sensor_button_press_event(data, expected_detect_wet):
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": data,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.detect_wet).is_equal_to(expected_detect_wet)

def test_leak_sensor_mic_mapping():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": 0,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.mic).is_equal_to("CRC")

def test_leak_sensor_id_mapping():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": 0,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.id).is_equal_to(0x1234)

def test_leak_sensor_model_mapping():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": 0,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.model).is_equal_to("Govee-Water")

def test_leak_sensor_battery_mv_mapping():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Battery Report",
        "battery_ok": 0.59,
        "battery_mV": 2508,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.battery_mV).is_equal_to(2508)

def test_leak_sensor_battery_level_mapping():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Battery Report",
        "battery_ok": 0.24,
        "battery_mV": 1812,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.battery_ok).is_equal_to(0.24)

@mark.parametrize("data, expected_battery_level", [(.01, BatteryLevel.EMPTY),
                                                  (.24, BatteryLevel.EMPTY),
                                                  (.25, BatteryLevel.LOW),
                                                  (.26, BatteryLevel.OK),
                                                  (None, BatteryLevel.UNKNOWN)])
def test_leak_sensor_battery_low(data, expected_battery_level):
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Battery Report",
        "battery_ok": data,
        "battery_mV": 1812,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.battery_level).is_equal_to(expected_battery_level)


def test_leak_sensor_water_leak_num_0():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Water Leak",
        "detect_wet": 1,
        "leak_num": 0,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.leak_num).is_equal_to(0)


def test_leak_sensor_water_leak_num_7():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Water Leak",
        "detect_wet": 1,
        "leak_num": 7,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.leak_num).is_equal_to(7)

@mark.parametrize("event, expected_event", [("Button Press", LeakSensorEvent.BUTTON_PRESS),
                                            ("Water Leak", LeakSensorEvent.WATER_LEAK),
                                            ("Battery Report", LeakSensorEvent.BATTERY_REPORT),
                                            ("Unknown", LeakSensorEvent.UNKNOWN),
                                            ("DOESNOTEXIST", LeakSensorEvent.INVALID)])
def test_leak_sensor_unkonown_event(event, expected_event):
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": event,
        "mic": "CRC",
        "time": "2024-06-01T12:00:00Z",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.event).is_equal_to(expected_event)

def test_leak_sensor_time_normalization():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": 0,
        "mic": "CRC",
        "time": "2026-05-15 10:30:00",
        "code": "0x01"
    }
    water_data = LeakSensor.from_dict(data)
    assert_that(water_data.time).is_equal_to("2026-05-15T10:30:00-04:00")

def test_leak_sensor_invalid_time():
    data = {
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "detect_wet": 0,
        "mic": "CRC",
        "time": "invalid time format",
        "code": "0x01"
    }
    try:
        LeakSensor.from_dict(data)
    except ValueError as e:
        assert_that(str(e)).contains("Invalid timestamp format: invalid time format")

def test_leak_sensor_to_dict():
    leak_sensor = LeakSensor(
        time="2024-06-01 12:00:00",
        model="Govee-Water",
        id=0x1234,
        event=LeakSensorEvent.BUTTON_PRESS,
        code="0x01",
        mic="CRC",
        detect_wet=0
    )
    dict_data = leak_sensor.to_dict()
    expected_data = {
        "time": "2024-06-01T12:00:00-04:00",
        "model": "Govee-Water",
        "id": 0x1234,
        "event": "Button Press",
        "code": "0x01",
        "mic": "CRC",
        "detect_wet": 0,
        "battery_ok": None,
        "battery_mV": None,
        "leak_num": None,
        "battery_level": 3
    }
    assert_that(dict_data).is_equal_to(expected_data)
