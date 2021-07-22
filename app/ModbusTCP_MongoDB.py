#!/usr/bin/env python
# -*- coding: utf-8 -*-
# read_register
# read 10 registers and print result on stdout

from pyModbusTCP.client import ModbusClient
import time
import requests
import json
from datetime import datetime
from app.MongoDB_Main import SensorDocument, ControllerDocument, DeviceDocument
from app.sensorDTO import sensorDto

# MongoDB
db_sensordoc = SensorDocument()
db_controllerdoc = ControllerDocument()
db_device = DeviceDocument()


def post(code):
    device = db_device.device_config()
    API_ENDPOINT = device[0]["API"]
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=code)
    # extracting response text
    pastebin_url = r.text
    # Response from Bosch URL
    if pastebin_url == "{}":
        print("Successfully Posted to Nexeed")
    else:
        print("URL Response: %s" % pastebin_url)


# Bosch TimeStamp Format
def timestamp():
    ts = datetime.now()
    time_zone = ts.astimezone()
    iso_format = time_zone.isoformat(timespec='milliseconds')
    time_stamp = iso_format.replace('+05:30', 'Z')
    return time_stamp


def modbus_tcp():
    regs = [15, 21, 23, 18, 21, 12, 16, 13]
    controller = db_controllerdoc.controller_config()[1]
    SERVER_HOST = controller["IPAddress"]
    SERVER_PORT = controller["Port"]
    print(SERVER_PORT,SERVER_HOST)

    c = ModbusClient()
    # uncomment this line to see debug message
    # c.debug(True)
    # define modbus server host, port
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    # MongoDB Sensor Document
    sensor = db_sensordoc.sensor_config()

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
    lists = []
    # if open() is ok, read register
    try:
        if c.is_open():
            # read 8 registers at address 0, store result in regs list
            regs = c.read_holding_registers(controller["RegisterAddress"], controller["RegisterLength"])
            print(type(regs[0]))
            # if success display registers
            if regs:
                print("reg ad #0 to 7: " + str(regs))

    except:
        print("Device is not Connected")

    # PPMP Format to be sent to API
    data = {
        "content-spec": "urn:spec://eclipse.org/unide/measurement-message#v3",
        "device": {
            "id": "ST10"
        },
        "measurements": [{
            "ts": timestamp(),
            "series": {
                "time": [0]
            }
        }]
    }

    sensor_data = []
    # Including Sensors data in PPMP Structure
    for i in range(0, len(regs)):
        mulvalue = float(10 / 65535)
        data["measurements"][0]["series"][i] = [regs[i] * mulvalue]
        json.dumps(data)
        sensorData = round(regs[i] * float(mulvalue), 3)
        sensor_data.append(sensorData)

        sensorName = ("sensor {}".format(i))
        sensorAddress = ("sensor Address {}".format(i))
        lists.append(sensorDto(sensorName, sensorAddress, str(sensorData)))

    # Converting objects into a json string
    jsondata = json.dumps(data)
    print(jsondata)

    # Push MongoDB
    db_sensordoc.field_config(sensor_data)
    try:
        # PPMP data is posted to Bosch Nexeed
        post(jsondata)
    except Exception as exception:
        print(exception)

        # Clearing the Sensor_Data List
    regs.clear()

    # sleep 2s before next polling
    # time.sleep(2)

    return lists

