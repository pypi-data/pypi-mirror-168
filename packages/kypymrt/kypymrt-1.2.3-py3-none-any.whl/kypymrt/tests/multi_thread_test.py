# -*- coding: utf-8 -*-
import random
import threading
import time
import os
import sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from kunyi_mrt import mrt_client
from kunyi_daq_monitor import Monitor
from kunyi_project import hil_project

# ipPro = hil_project(r'D:\work\EE\pymrt\port_yn\Build\ipyn3.ipr')
ipPro = hil_project(r'ip_projects/Build_folder/IntegratePortal0816.ipr')
file_path = ipPro.build_zip()
host = "192.168.5.18"
mt = Monitor(host=host, file_path=file_path)
mt2 = Monitor(host=host, file_path=file_path)

def test_init():

    # ipPro = os.path.abspath('ip_projects/Build_folder/IntegratePortal0816.ipr')
    # ipPro = hil_project(r'D:\work\EE\pymrt\port_yn\Build\ipyn3.ipr')

    inPortList, outPortList = ipPro.get_ports(instanceName="Expression_1")
    mt.config_monitor(port_number=6, is_queue=0, period_ms=100)
    mt.set_ports_to_monitor(inPortList, start_port=0,end_port=2)
    mt.set_ports_to_monitor(outPortList, start_port=0,end_port=2, alreadySetportNum=2)
    mt.startDaq()

def test_set_PortValue():
    successCount = 0
    failCount = 0
    sumCount = 0
    fileNum = 1
    ecCount = 0
    while True:
        time.sleep(1)
        portValue = random.randint(1,50)
        setec = mt.set_PortValue("Expression_1", "x[0]", "Double", portValue, item_count=1, sub_struct_detail=None)
        time.sleep(2)
        value,getec = mt.getport_value("Expression_1", "y[0]", "Double", item_count=1)
        if setec==0 or getec ==0:
            ecCount +=1
        if ecCount >=3:
            return
        if setec==1 and getec ==1:
            ecCount = 0
        with open(f"./infoFile/setValueMsg_{fileNum}.txt", "a") as f:
            if value == portValue:
                successCount += 1
                sumCount +=1
                setValueMsg = (f"successTime:{time.strftime('%m%d_%H%M_%S')}**successCount:{successCount}--sum{sumCount}\n")
                f.write(setValueMsg)
                print(setValueMsg)
            else:
                sumCount +=1
                failCount += 1
                setValueMsg = (f"failTime:{time.strftime('%m%d_%H%M_%S')}**failCount:{failCount}--sum{sumCount}\n")
                f.write(setValueMsg)
                print(setValueMsg)
        statinfo = os.stat(f"./infoFile/setValueMsg_{fileNum}.txt")
        if statinfo.st_size >= 1073741824:  # 10M
            fileNum +=1

def test_read():
    ecCount = 0
    while True:
        time.sleep(1)
        ec = mt.monitor(monitor_period_s=1, value_list_size=2, item_count=1, sub_struct_detail=None)
        if ec == 0:
            ecCount += 1
        else:
            ecCount = 0
        if ecCount >= 3:
            return

def test_read2():
    ecCount = 0
    while True:
        time.sleep(1)
        ec = mt2.monitor(monitor_period_s=1, value_list_size=2, item_count=1, sub_struct_detail=None)
        if ec == 0:
            ecCount += 1
        else:
            ecCount = 0
        if ecCount >= 3:
            return

def test_stop_env():
    test_init()
    time.sleep(10)
    env_name ="env01"
    mrt2 = mrt_client(host="192.168.5.18")
    mrt2.connet()
    with open("./daqinfo.txt", "r") as f:
        d = int(f.read())

    ec2=mrt2.stop_test(env_name)
    time.sleep(3)
    mrt2.start_test(env_name)
    time.sleep(10)

    # mt.stop_daq(env_name,d)
    mt.stop_test(env_name)

def test_Thread():
    test_init()
    t1 = threading.Thread(target=test_set_PortValue)
    t1.start()
    t2 = threading.Thread(target=test_read)
    t2.start()

# test_Thread()
