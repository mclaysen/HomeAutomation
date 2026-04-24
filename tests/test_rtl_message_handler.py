from assertpy import assert_that
from tests.fake_mqttsubscriber import FakeMqttPublisher
from mqttHandlers.messageHandlers.rtlMessageHandler import RtlMessageHandler
from models.sensorMappings import Config

def test_rtl_message_handler_init():
    rtl = FakeMqttPublisher()
    configTest = Config(ModelMappings=[])
    handler = RtlMessageHandler(rtl, configTest, rtl, None)

