import os
import pytest
from tests.tools.build_env import *


@pytest.fixture
def mqtt_monitor_client():
    mqtt_monitor_client = SoPMQTTMonitor()
    # mqtt_monitor_client.run()
    return mqtt_monitor_client


@pytest.fixture
def mqtt_monitor_client_level1():
    mqtt_monitor_client = SoPMQTTMonitor(
        name='level1_monitor', host='127.0.0.1', port=11883)
    # mqtt_monitor_client.run()
    return mqtt_monitor_client


@pytest.fixture
def mqtt_monitor_client_level2():
    mqtt_monitor_client = SoPMQTTMonitor(
        name='level2_monitor', host='127.0.0.1', port=21883)
    # mqtt_monitor_client.run()
    return mqtt_monitor_client


@pytest.fixture
def mqtt_monitor_client_level3():
    mqtt_monitor_client = SoPMQTTMonitor(
        name='level3_monitor', host='127.0.0.1', port=31883)
    # mqtt_monitor_client.run()
    return mqtt_monitor_client
