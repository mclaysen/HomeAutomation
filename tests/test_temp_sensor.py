from models.temp_sensor import TempSensorData
from assertpy import assert_that

def test_temp_sensor_data_from_dict():
    data = {
        "time": "2026-01-15 10:30:00",
        "model": "TempSensorX",
        "id": 123,
        "channel": "A",
        "battery_ok": 1,
        "temperature_C": 22.5,
        "humidity": 45,
        "mic": "abc123"
    }
    temp_data = TempSensorData.from_dict(data)

    assert_that(temp_data.time).is_equal_to("2026-01-15T10:30:00-05:00")
    assert_that(temp_data.model).is_equal_to("TempSensorX")
    assert_that(temp_data.id).is_equal_to(123)
    assert_that(temp_data.channel).is_equal_to("A")
    assert_that(temp_data.battery_ok).is_equal_to(1)
    assert_that(temp_data.temperature_C).is_equal_to(22.5)
    assert_that(temp_data.humidity).is_equal_to(45)
    assert_that(temp_data.mic).is_equal_to("abc123")