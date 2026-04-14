from assertpy import assert_that
from models.water_sensor import WaterSensorData

def test_water_sensor_data_from_dict():
    data = {
        "time": "2026-01-15 10:30:00",
        "model": "WaterSensorX",
        "id": 456,
        "event": "leak_detected",
        "code": "WET",
        "mic": "def456",
        "detect_wet": True,
        "battery_ok": 0.8,
        "battery_mV": 3000,
        "leak_num": 1
    }
    water_data = WaterSensorData.from_dict(data)

    assert_that(water_data.time).is_equal_to("2026-01-15T10:30:00-05:00")
    assert_that(water_data.model).is_equal_to("WaterSensorX")
    assert_that(water_data.id).is_equal_to(456)
    assert_that(water_data.event).is_equal_to("leak_detected")
    assert_that(water_data.code).is_equal_to("WET")
    assert_that(water_data.mic).is_equal_to("def456")
    assert_that(water_data.detect_wet).is_true()
    assert_that(water_data.battery_ok).is_equal_to(0.8)
    assert_that(water_data.battery_mV).is_equal_to(3000)
    assert_that(water_data.leak_num).is_equal_to(1)