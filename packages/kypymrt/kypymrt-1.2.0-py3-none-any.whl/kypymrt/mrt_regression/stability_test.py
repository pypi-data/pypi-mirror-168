# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import random
import sys
import threading
import time

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from kunyi_hil_test import hil_test, meta_format
from kunyi_mrt import mrt_client
from kunyi_util import kunyi_util



def test_init():
    rtpc_client = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ip_project_path = fr'{rootpath}/tests/ip_projects/Build_folder/IntegratePortal0816.ipr'
    env_name = "env_2"
    mytest = hil_test(ip_project_path, rtpc_client, env_name)
    all_input_ports = mytest.list_input_ports("Expression_1", format=meta_format.meta_tuple)
    return mytest ,all_input_ports

def test_updateValue(mytest ,all_input_ports):
    successCount = 0
    failCount = 0
    sumCount = 0
    fileNum = 1
    ecCount = 0
    try:
        mytest.prepare_test_env()
        mytest.start_test()
        mytest.monitor_signals(all_input_ports)
        mytest.signal_daq.fetch_period = 0.5
        while True:
            portValue = random.randint(1,50)
            sec = mytest.update_input_port_values("Expression_1", "x[0]", "Double", portValue, item_count=1, sub_struct_detail=None)
            time.sleep(2)
            value,getec = mytest.getport_value("Expression_1", "y[0]", "Double", item_count=1)
            if sec == 0 or getec == 0:
                ecCount += 1
            if ecCount >= 3:
                return
            if sec == 1 and getec == 1:
                ecCount = 0
            with open(f"{r}/regression_info/setValueMsg_{fileNum}.msg", "a") as f:
                if value == portValue:
                    successCount += 1
                    sumCount += 1
                    setValueMsg = (
                        f"successTime:{time.strftime('%m%d_%H%M_%S')}**successCount:{successCount}--sum{sumCount}\n")
                    f.write(setValueMsg)
                    print(setValueMsg)
                else:
                    sumCount += 1
                    failCount += 1
                    setValueMsg = (f"failTime:{time.strftime('%m%d_%H%M_%S')}**failCount:{failCount}--sum{sumCount}\n")
                    f.write(setValueMsg)
                    print(setValueMsg)
            statinfo = os.stat(f"{r}/regression_info/setValueMsg_{fileNum}.msg")
            if statinfo.st_size >= 1073741824:  # 10M
                fileNum += 1
    finally:
        mytest.close()
        print(f"endTime:{time.strftime('%m%d_%H%M_%S')}")

def test_read(mytest,all_input_ports):
    while True:
        time.sleep(1)
        values = mytest.fetch_values(all_input_ports)
        print(values)

def test_Thread():
    mytest ,all_input_ports = test_init()
    t1 = threading.Thread(target=test_updateValue , args=(mytest,all_input_ports))
    t1.start()
    t2 = threading.Thread(target=test_read,args=(mytest,all_input_ports))
    t2.start()