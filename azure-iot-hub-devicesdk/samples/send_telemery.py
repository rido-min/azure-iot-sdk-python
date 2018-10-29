# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import logging
from azure.iot.hub.devicesdk.device_client import DeviceClient
from azure.iot.hub.devicesdk.auth.authentication_provider_factory import from_connection_string

logging.basicConfig(level=logging.INFO)

conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
auth_provider = from_connection_string(conn_str)
simpleDevice = DeviceClient.from_authentication_provider(auth_provider, "mqtt")


def connection_state_callback(status):
    print("connection status: " + status)
    if status == "connected":
        simpleDevice.send_event("Mimbulus Mimbletonia")


simpleDevice.on_connection_state = connection_state_callback
simpleDevice.connect()

while True:
    continue
