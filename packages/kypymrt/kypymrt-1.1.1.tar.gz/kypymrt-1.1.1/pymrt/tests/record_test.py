# -*- coding: utf-8 -*-
import time
import os
import sys

from kunyi_util import *

r = os.path.abspath(os.path.dirname(__file__))
rootpath = os.path.split(r)[0]
sys.path.append(rootpath)
from kunyi_daq_monitor import Monitor
from kunyi_project import hil_project

# file_path = os.path.abspath('ip_projects/Build.zip')
file_path = r"D:\work\EE\rtpc_testIP\255\Build.zip"
host = "192.168.5.18"
mt = Monitor(host=host, file_path=file_path)


def test_record():
    ipPro = hil_project(r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr')
    inPortList, outPortList = ipPro.get_ports(instanceName="Expression_2")
    mt.config_monitor(port_number=6, is_queue=0, period_ms=100)
    mt.set_ports_to_monitor(inPortList, start_port=0, end_port=3)
    mt.set_ports_to_monitor(outPortList, start_port=0, end_port=3, alreadySetportNum=3)
    mt.startDaq()
    while True:
        time.sleep(1)
        trigger_start = ("Expression_2", "x[0]", ">=", 30)
        trigger_stop = ("Expression_2", "x[0]", ">=", 10000000)
        # trigger_stop =("Expression_2", "x[0]", "between", 50,40000) #between
        mt.saveTotemp(isTrigger=True, trigger_start=trigger_start, trigger_stop=trigger_stop)


def test_record_temp_parse(tmpFilePath="./dataRecordTemp/dataRecord_1.tmp", signalType="Double", recodePortNum=6):
    with open(tmpFilePath, "rb") as f:
        bytes = f.read()
    with open(f"./infoFile/PortMsg.txt", "r") as f:
        ports_info = eval(f.read())
        for portinfo in ports_info.values():
            pass
    buf_read_idx = 0
    parseCount = 0
    snT = signalType
    while True:
        try:
            item_size = 8
            if parseCount == 0:
                signalType = "UInt64"
            else:
                signalType = snT
            item_data_buf = bytes[buf_read_idx: buf_read_idx + item_size]
            item_data_value = kunyi_util.bytes_to_data(signalType, item_data_buf, item_count=1, struct_detail=None)
            if signalType == "UInt64":
                print(item_data_value)
            else:
                for port in portinfo:
                    print(f"{port[0]}_{port[1]}:{item_data_value}")
            buf_read_idx = buf_read_idx + item_size
            parseCount += 1
            if parseCount - 1 == recodePortNum:
                parseCount = 0
        except:
            print("Parsing is complete")
            return
