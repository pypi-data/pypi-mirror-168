# -*- coding: utf-8 -*-
import os
import time

from kunyi_daq_monitor import Monitor
from kunyi_project import hil_project
from kunyi_mrt import mrt_client


class Test_M:

    ipPro = hil_project(r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr')
    file_path = ipPro.build_zip()
    host = "192.168.5.18"
    env_name = "env066"
    mt = Monitor(host=host, file_path=file_path,env_name=env_name)
    inPortList, outPortList = ipPro.get_ports(instanceName="Expression_2")

    def test_monitor(self):

        '''
       Enter the instance name to resolve the port under the current instance
        '''
        self.mt.set_PortValue("Expression_2", "x[0]", "Double", 1.56, item_count=1, sub_struct_detail=None)
        self.mt.config_monitor(port_number=2, is_queue=0, period_ms=100)
        self.mt.set_ports_to_monitor(self.inPortList, start_port=0, end_port=1)
        self.mt.set_ports_to_monitor(self.outPortList, start_port=0, end_port=1, alreadySetportNum=1)
        self.mt.startDaq()
        while True:
            # time.sleep(0.5)
            self.mt.monitor(monitor_period_s=1, value_list_size=2, item_count=1, sub_struct_detail=None)

    def test_stop_env(self):
        env_name = "env01"
        mrt = mrt_client(host="192.168.5.18")
        mrt.connet()
        with open("./daqinfo.txt", "r") as f:
            d = int(f.read())
        ec1 = mrt.stop_daq(env_name, d)
        ec2 = mrt.stop_test(env_name)
        if ec1.value != 0 and ec2 != 0:
            isconfirm = input("The experimental environment is abnormal!\n Are you sure about the destruction? (y/n):")
            if isconfirm.lower() == "y":
                mrt.destroy_daq(env_name, d)
                mrt.delete_test_env(env_name)
                print("The experimental environment is abnormal and has been destroyed！")
            else:
                pass

    def test_destroytest(self):
        with open("./daqinfo.txt", "r") as f:
            d = int(f.read())
        self.mt.destroy_daq(self.env_name, d)
        self.mt.delete_test_env(self.env_name)

