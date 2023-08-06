# -*- coding: utf-8 -*-
import argparse
import os
import sys
import time

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from kunyi_hil_test import hil_test, meta_format
from kunyi_mrt import mrt_client

parser = argparse.ArgumentParser(description='mrtTest')
parser.add_argument('-host', type=str, default = "127.0.0.1",help="mrt host(default:127.0.0.1)")
parser.add_argument('-n', type=str, default="env01",help="Create a new test enviroment with name "
                                                         "of env_name (default:env01)")
parser.add_argument('-m', type=int, default=8888,help="Specify runtime manager server address or port(default:8888)")
parser.add_argument('-p', type=int, default=8889,help="Specify the publish message server address or port(default:8889)")
parser.add_argument('-s', type=int, default=8890,help="Specify the subscribe message server address or "
                                                      "port(default:8890)")
parser.add_argument('-ipr', type=str, default=None,help="ip project *.ipr file path")
parser.add_argument('-ins', type=str, default="Expression_1",help="A model instance(default:Expression_1)")
parser.add_argument('-begin', type=int, default=0,help="Start signal list index(default:0)")
parser.add_argument('-end', type=int, default=None,help="End signal list index(default:None)")
parser.add_argument('-dp', type=float, default=0.5,help="daq period (default:0.5)")
parser.add_argument('-fp', type=float, default=0.5,help="fetchValue period(default:0.5)")

args = parser.parse_args()

def test_daq_releated(keepTime = 3600*48):# 1h=3600s 1day = 1h*24
    rtpc_client = mrt_client(args.host, args.m, args.p, args.s)
    ip_project_path = args.ipr
    env_name = args.n
    mytest = hil_test(ip_project_path, rtpc_client, env_name)
    t=0
    fileNum = 1
    try:
        mytest.prepare_test_env()
        mytest.start_test()
        all_input_ports = mytest.list_input_ports(args.ins, format=meta_format.meta_tuple)
        mytest.monitor_signals(all_input_ports[0:5])
        mytest.signal_daq.fetch_period = args.dp
        infoFileDir = os.path.join(r, "regression_info")
        if not os.path.exists(infoFileDir):
            os.mkdir(infoFileDir)
        with open(f"{infoFileDir}/signal_info_{fileNum}.info", "a") as f:

            while True:

                all_values = mytest.fetch_values(all_input_ports[args.begin:args.end])
                f.write(str(all_values)+"\n")
                print(all_values)
                st = args.fp
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
test_daq_releated()