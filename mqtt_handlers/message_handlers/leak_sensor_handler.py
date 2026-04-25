import logging
from models.sensor_mappings import Config
from mqtt_handlers.subscriber_model import SubscriberModel
from typing import TypeVar
from mqtt_handlers.mqtt_publisher import MqttPublisher
import json
from models.leak_sensor import LeakSensor, LeakSensorEvent

T = TypeVar('T')


class LeakSensorHandler:
    def __init__(self, subscriberData: SubscriberModel,  appSettings: Config,  publisher: MqttPublisher, logger: logging.Logger):
        self.appSettings = appSettings
        self.publisher = publisher
        self.logger = logger
        self.deviceType = subscriberData.deviceType

    def _get_battery_report_payload(self, payload: LeakSensor) -> dict:
        return {
            "id": payload.id,
            "model": payload.model,
            "time": payload.time,
            "event": payload.event.value,
            "battery": payload.battery_ok,
            "battery_level": payload.battery_level.value,
            "battery_mV": payload.battery_mV
        }

    def _get_leak_report_payload(self, payload: LeakSensor) -> dict:
        return {
            "id": payload.id,
            "model": payload.model,
            "time": payload.time,
            "event": payload.event.value,
            "detect_wet": payload.detect_wet,
            "leak_num": payload.leak_num
        }

    def _get_button_click_report_payload(self, payload: LeakSensor) -> dict:
        return {
            "id": payload.id,
            "model": payload.model,
            "time": payload.time,
            "event": payload.event.value
        }

    def on_message(self, payload: LeakSensor) -> None:
        self.logger.debug(payload)

        leak_model = next((model for model in self.appSettings.ModelMappings if model.model == payload.model), None)
        if leak_model is not None:
            sensor = next((sensor for sensor in leak_model.sensors if sensor.id == payload.id), None)
            if sensor is not None:
                topic_prefix = f"rtl_433/leak_sensor/{sensor.name}"
                if payload.event == LeakSensorEvent.BATTERY_REPORT:
                    report_payload = self._get_battery_report_payload(payload)
                    self.publisher.publish(f"{topic_prefix}/battery_report", json.dumps(report_payload), 0, False)
                elif payload.event == LeakSensorEvent.WATER_LEAK:
                    leak_payload = self._get_leak_report_payload(payload)
                    battery_payload = self._get_battery_report_payload(payload)
                    self.publisher.publish(f"{topic_prefix}/leak_report", json.dumps(leak_payload), 0, False)
                    self.publisher.publish(f"{topic_prefix}/battery_report", json.dumps(battery_payload), 0, False)
                elif payload.event == LeakSensorEvent.BUTTON_PRESS:
                    click_payload = self._get_button_click_report_payload(payload)
                    leak_payload = self._get_leak_report_payload(payload)
                    battery_payload = self._get_battery_report_payload(payload)
                    self.publisher.publish(f"{topic_prefix}/leak_report", json.dumps(leak_payload), 0, False)
                    self.publisher.publish(f"{topic_prefix}/battery_report", json.dumps(battery_payload), 0, False)
                    self.publisher.publish(f"{topic_prefix}/button_click_report", json.dumps(click_payload), 0, False)
                else:
                    self.logger.warning("Unknown event type: %s", payload.event.value)
            else:
                self.logger.warning("No sensor found for %s", payload.id)