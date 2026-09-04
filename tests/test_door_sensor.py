from assertpy import assert_that

from models.door_sensor import DoorSensor


def test_door_sensor_from_dict_custom_door_sensor():
    payload_obj = {
        "time": "2026-09-03 22:40:46",
        "model": "Generic-Remote",
        "id": 30409,
        "cmd": 14,
        "tristate": "Z1ZX10XZ001X",
    }

    output = DoorSensor.from_dict(payload_obj)
    assert_that(output.id).is_equal_to(30409)
    assert_that(output.time).is_equal_to("2026-09-03 22:40:46")
    assert_that(output.model).is_equal_to("Custom-Door-Sensor")
    assert_that(output.command).is_equal_to(14)
    assert_that(output.tri_state).is_equal_to("Z1ZX10XZ001X")


def test_door_sensor_from_dict_generic_remote():
    payload_obj = {
        "time": "2026-09-03 22:40:46",
        "model": "Generic-Remote",
        "id": 12345,
        "cmd": 14,
        "tristate": "Z1ZX10XZ001X",
    }

    output = DoorSensor.from_dict(payload_obj)
    assert_that(output.id).is_equal_to(12345)
    assert_that(output.time).is_equal_to("2026-09-03 22:40:46")
    assert_that(output.model).is_equal_to("Generic-Remote")
    assert_that(output.command).is_equal_to(14)
    assert_that(output.tri_state).is_equal_to("Z1ZX10XZ001X")
