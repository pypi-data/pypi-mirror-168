# -*- coding: utf-8 -*-
import os
import sys
import time
r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from kunyi_hil_test import hil_test, meta_format
from kunyi_mrt import mrt_client


def test_daq_releated(keepTime = 3600*48):# 1h=3600s 1day = 1h*24
    rtpc_client = mrt_client("192.168.3.90", "8888", "8889", "8890")
    ip_project_path = r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr'
    # ip_project_path = r'D:\work\EE\rtpc_testIP\0cc\mattest4.ipr'
    env_name = "env_mat"
    mytest = hil_test(ip_project_path, rtpc_client, env_name)
    t=0
    fileNum = 1
    try:
        mytest.prepare_test_env()
        mytest.start_test()
        all_input_ports = mytest.list_input_ports("Expression_2", format=meta_format.meta_tuple)
        mytest.monitor_signals(all_input_ports[0:None])
        mytest.signal_daq.fetch_period = 0.5
        infoFileDir = os.path.join(r,"regression_info")
        if not os.path.exists(infoFileDir):
            os.mkdir(infoFileDir)
        with open(f"{infoFileDir}/signal_info_{fileNum}.info", "a") as f:

            while True:

                all_values = mytest.fetch_values(all_input_ports[0:5])
                f.write(str(all_values)+"\n")
                print(all_values)
                st = 0.2
                time.sleep(st)
                t += st
                if t >= keepTime:
                    return
                statinfo = os.stat(f"{infoFileDir}/signal_info_{fileNum}.info")
                if statinfo.st_size >= 1073741824:  # 10M
                    fileNum += 1
    finally:
        mytest.close()
        print(f"endTime:{time.strftime('%m%d_%H%M_%S')}")