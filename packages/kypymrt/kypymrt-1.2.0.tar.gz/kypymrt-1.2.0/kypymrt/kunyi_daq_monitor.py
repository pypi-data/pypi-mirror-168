import os
import sys
import time
from pprint import pprint,pformat

from Enums import mrt_port_type_t
from kunyi_mrt import mrt_client
# r=os.path.abspath(os.path.dirname(__file__))
# rootpath=os.path.split(r)[0]
# sys.path.append(rootpath)
class Monitor(mrt_client):
    def __init__(self,host, managerment_port=8888, push_port=8889, subscription_port=8890,env_name="env01",file_path=""):
        super().__init__(host, managerment_port, push_port, subscription_port)
        self.env_name = env_name
        self.host = host
        self.file_path = file_path
        self.mgr_port = managerment_port
        self.push_port = push_port
        self.subs_port = subscription_port
        self.signal_values = {}
        self._pt_list = ["INPUT_PORT",
                    "OUTPUTPORT",
                    "MEASUREMENT",
                    "UNKNOWN_PORT"]
        self._signal_inPortValue_list = []
        self._signal_outPortValuelist = []
        self._signal_measurementValuelist = []
        self.daq_handle = None
        self.connet()
        ec,ei = self.get_env_info(self.env_name)
        running_status = ei.contents.running_status
        if running_status !=1:
            self.create_test_env(self.env_name)
            ec,file_id = self.download_file(self.file_path)
            while True:
                value = mrt_client.dispatch_progress
                print("\rThe lab package is being delivered...")
                if value >= 1 and file_id > 0:
                    print("Issued by the successful!")
                    break
            self.load_test_resources_to_env(self.env_name, file_id)
            self.start_test(self.env_name)
            self.config_monitor()
        if running_status ==1:
            with open("./daqinfo.txt","r") as f:
                print("\nReconnection daq...")
                self.daq_handle = int(f.read())

    def set_PortValue(self,instance_name, port_name, signal_type,signal_value,item_count, struct_detail=None, **sub_struct_detail):
        rc = self.set_input_port_value(self.env_name, instance_name, port_name, signal_type,signal_value,item_count, struct_detail, **sub_struct_detail)
        type_dict = {"Int8": 1,
                     "Int16": 2,
                     "Int32": 4,
                     "Int64": 8,
                     "UInt8": 1,
                     "UInt16": 2,
                     "UInt32": 4,
                     "UInt64": 8,
                     "Float": 4,
                     "Double": 8,
                     "Bool": 1,
                     "ASCII": 2000,
                     "UTF8": 2000}
        expect_size = type_dict[signal_type]
        if rc == expect_size:
            print("Set the value successfully.")
            return 1
        else:
            print("Failed to set the value")
            return 0

    def getport_value(self,instance_name, port_name, signal_type,item_count):
        rc,value= self.get_output_port_value(self.env_name, instance_name, port_name, signal_type,item_count,)
        type_dict = {"Int8": 1,
                     "Int16": 2,
                     "Int32": 4,
                     "Int64": 8,
                     "UInt8": 1,
                     "UInt16": 2,
                     "UInt32": 4,
                     "UInt64": 8,
                     "Float": 4,
                     "Double": 8,
                     "Bool": 1,
                     "ASCII": 2000,
                     "UTF8": 2000}
        expect_size = type_dict[signal_type]
        if rc == expect_size:
            print("Get the value successfully.")
            return value , 1
        else:
            print("Failed to get the value")
            return None , 0

    def config_monitor(self,  port_number=2, is_queue=0, period_ms=100, offset_ms=1):
        ec,self.daq_handle = self.create_daq(self.env_name, port_number, is_queue)
        self.daq_set_trigger_period(self.env_name, self.daq_handle, period_ms, offset_ms)

    def set_ports_to_monitor(self,portlist,start_port=0,end_port=None,alreadySetportNum=0):
        '''

        :param portlist:
        :param start_port: Which port to start with
        :param end_port:Which port to end from
        :param alreadySetportNum:The port has been set
        :return:
        '''
        ports = portlist[start_port:end_port]
        port_index = 0 + alreadySetportNum
        for port in ports:
            model_instance_name, port_name, port_type, port_datatype = port
            if self.daq_handle == None:
                raise Exception("config_monitor() it's not run")
            self.daq_set_port(self.env_name,self.daq_handle,port_index, model_instance_name,
                            port_name, port_type, port_datatype)
            port_index +=1

    def startDaq(self):
        self.start_daq(self.env_name, self.daq_handle)

    def saveTotemp(self,isTrigger,trigger_start=None,trigger_stop=None):
        self.daq_write_temp(self.env_name, self.daq_handle,item_count = 1,isTrigger=isTrigger,
                            trigger_start=trigger_start,trigger_stop=trigger_stop)

    def monitor(self,monitor_period_s,value_list_size,item_count,sub_struct_detail):
        fileNum = 1
        with open (f"./infoFile/monitor_msgs_{fileNum}.txt","a") as f:
            # while True:
            time.sleep(monitor_period_s)
            msg_list = self.daq_read(self.env_name,self.daq_handle,item_count,sub_struct_detail)
            if msg_list is None:
                msg_listInfo = (f"{time.strftime('%m%d_%H%M_%S')}:Daq read failure , Please reconnect\n.")
                with open("./infoFile/msg_readInfo.txt", "a") as f:
                    f.write(msg_listInfo)
                    f.flush()
                return 0
            for port_list in msg_list:
                for signal_msg in port_list:
                    pt_index = signal_msg[2]
                    pt = self._pt_list[pt_index]
                    port_name = signal_msg[1]
                    # signal_defin = f"{signal_msg[0]}_{port_name}_{pt}"
                    signal_defin = (signal_msg[0],port_name,pt)
                    t = time.strftime("%Y%m%d_%H%M_%S", time.localtime(signal_msg[4] / 1000000))
                    if pt == "INPUT_PORT":
                        signal_value = (f"{signal_msg[3]}",f"{t}")
                        self._signal_inPortValue_list.append(signal_value)
                        self.signal_values[signal_defin] = self._signal_inPortValue_list
                    elif pt == "OUTPUTPORT":
                        signal_value = (f"{signal_msg[3]}",f"{t}")
                        self._signal_outPortValuelist.append(signal_value)
                        self.signal_values[signal_defin] = self._signal_outPortValuelist
                    elif pt == "MEASUREMENT":
                        signal_value = (f"{signal_msg[3]}",f"{t}")
                        self._signal_measurementValuelist.append(signal_value)
                        self.signal_values[signal_defin] = self._signal_measurementValuelist
                    else:
                        raise Exception("UNKNOWN_PORT")
            for vlist in self.signal_values.values():
                if len(vlist) > value_list_size:
                    while len(vlist) > value_list_size:
                        del vlist[0]
            monitor_msgs = self.signal_values
            f.write(f"{time.strftime('%m%d_%H%M_%S')}:***{pformat(str(monitor_msgs))}\n")
            f.flush()
            statinfo = os.stat(f"./infoFile/monitor_msgs_{fileNum}.txt")
            if statinfo.st_size >= 1073741824:  # 10M
                fileNum += 1
            pprint(monitor_msgs)






