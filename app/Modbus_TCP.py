#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read_register
# read 10 registers and print result on stdout

from pyModbusTCP.client import ModbusClient
import time
import requests
import json

from datetime import datetime

from app.sensorDTO import sensorDto

SERVER_HOST = "192.168.1.40"
SERVER_PORT = 502

c = ModbusClient()

# uncomment this line to see debug message
# c.debug(True)

# define modbus server host, port
c.host(SERVER_HOST)
c.port(SERVER_PORT)


def post(code):
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
    regs = [45, 191, 23, 18, 21, 12, 16, 13]

    # open or reconnect TCP to server
    if not c.is_open():
        if not c.open():
            print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))

    # if open() is ok, read register (modbus function 0x03)
    if c.is_open():
        # read 8 registers at address 0, store result in regs list
        regs = c.read_holding_registers(reg_addr=0, reg_nb=8)
        # print(type(regs[0]))
        # if success display registers
        if regs:
            print("reg ad #0 to 7: " + str(regs))

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

    list = []
    #
    #
    # list.append(sensorDto("huinity1", 10, 1))
    # list.append(sensorDto("huinity2", 10, 1))
    sensor_data = []
    # Including Sensors data in PPMP Structure
    for i in range(0, len(regs)):
        mulvalue = 10/65535
        data["measurements"][0]["series"][i] = [regs[i]*float(mulvalue)]
        json.dumps(data)
        sensorData = round(regs[i]*float(mulvalue),3)
        sensor_data.append(sensorData)
        sensorName = ("sensor {}".format(i))
        sensorAddress = ("sensor Address {}".format(i))
        list.append(sensorDto(sensorName, sensorAddress, sensorData))

    # Converting objects into a json string
    jsondata = json.dumps(data)
    print(jsondata)

        # PPMP data is posted to Bosch Nexeed
        # post(jsondata)

        # Clearing the Sensor_Data List
        # regs.clear()

        # sleep 2s before next polling
        # time.sleep(2)

    return list
