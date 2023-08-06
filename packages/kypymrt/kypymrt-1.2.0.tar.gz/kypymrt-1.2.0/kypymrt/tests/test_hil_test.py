from kunyi_hil_test import *
from kunyi_mrt import *
from Enums import *


def test_basic():
    rtpc_client = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ip_project_path = r'C:\Users\windy\Documents\IntegratePortal0816\.ip\Build\IntegratePortal0816.ipr'
    # ip_project_path = r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr'
    mytest = hil_test(ip_project_path, rtpc_client, "6666")
    env_name = "qpsithhpzp"

    #env_name = mytest.prepare_test_env()
    #ec = mytest.start_test()
    ec = mytest.is_test_running()
    time.sleep(1)

    mytest.enable_logging("./temp")
    mytest.list_instances()


    while True:
        print(str(mytest.is_test_running()))
        ports = {"Expression_1": "y[0]"}
        all_values = mytest.fetch_output_ports_values(ports)
        time.sleep(10)

def test_daq_releated():
    rtpc_client = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ip_project_path = r'C:\Users\windy\Documents\IntegratePortal0902\.ip\Build\IntegratePortal0902.ipr'
    # ip_project_path = r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr'
    env_name = "windy"
    mytest = hil_test(ip_project_path, rtpc_client, env_name)
    try:
        mytest.prepare_test_env()
        mytest.start_test()
        all_input_ports4 = mytest.list_input_ports("Expression_3", format=meta_format.meta_tuple)
        mytest.monitor_signals(all_input_ports4)
        mytest.signal_daq.fetch_period = 2

        while True:

            all_values = mytest.fetch_values(all_input_ports4)
            print(all_values)
            time.sleep(0.1)
    finally:
        mytest.close()





def test_project_related():
    rtpc_client = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ip_project_path = r'C:\Users\windy\Documents\IntegratePortal0902\.ip\Build\IntegratePortal0902.ipr'
    # ip_project_path = r'D:\work\EE\rtpc_testIP\255\Build\ip812255.ipr'
    mytest = hil_test(ip_project_path, rtpc_client, "qpsithhpzp")
    all_input_ports1 = mytest.list_input_ports("Expression_3")
    all_input_ports2 = mytest.list_input_ports("Expression_3", format=meta_format.name_only)
    all_input_ports3 = mytest.list_input_ports("Expression_3", format=meta_format.meta_dict)
    all_input_ports4 = mytest.list_input_ports("Expression_3", format=meta_format.meta_tuple)

    all_out_ports1 = mytest.list_output_ports("Expression_3")
    all_out_ports2 = mytest.list_output_ports("Expression_3", format=meta_format.name_only)
    all_out_ports3 = mytest.list_output_ports("Expression_3", format=meta_format.meta_dict)
    all_out_ports4 = mytest.list_output_ports("Expression_3", format=meta_format.meta_tuple)
    print("haha")


