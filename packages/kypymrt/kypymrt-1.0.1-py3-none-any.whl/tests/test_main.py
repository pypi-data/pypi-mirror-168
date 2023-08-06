import os.path
import time

from kunyi_mrt import *



def test_mrt_apis():
    my_mrt = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ec = my_mrt.connet()
    assert ec.value == 0
    ec = my_mrt.create_test_env("test1")
    assert ec.value == 0

    # ec = my_mrt.delete_test_env("test1")

    ec, name = my_mrt.get_env_name_by_idx(0)
    assert ec.value == 0
    assert name == "test1"

    ec, num = my_mrt.get_env_number()
    assert ec.value == 0
    assert num == 1

    pf_path = os.path.abspath('ip_projects/Build.zip')
    # pf_path = r"D:\work\EE\pymrt\port_yn\Build.zip"
    ec, file_id = my_mrt.download_file(pf_path)
    assert ec.value == 0
    time.sleep(1)
    while True:
        value = mrt_client.dispatch_progress
        if value >= 1:
            break

    assert value == 1

    my_mrt.load_test_resources_to_env("test1", file_id)

    ec = my_mrt.start_test("test1")
    assert ec.value == 0
    ec, info = my_mrt.get_env_info("test1")
    assert info.contents.running_status == 1

    rc = my_mrt.set_input_port_value("test1", "Expression_1", "x[0]", "Double", 1.1,item_count=1,struct_detail=None)
    assert rc == 8

    time.sleep(5)

    rc, value = my_mrt.get_output_port_value("test1", "Expression_1", "y[0]", "Double",item_count=1)
    assert rc == 8
    # assert value == 120.45


    ec, daq_handle = my_mrt.create_daq("test1", 2, 0)

    assert ec.value == 0, "resValue:{}".format(ec.value)

    # get_daq_info
    ec, daqinfo1 = my_mrt.get_daq_info("test1", daq_handle)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.daq_set_trigger_period("test1", daq_handle, 1, 1)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec, daqinfo2 = my_mrt.get_daq_info("test1", daq_handle)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.daq_set_port("test1", daq_handle, 0, "Expression_1", "x[0]",
                             mrt_port_type_t.MRT_INPUT_PORT, "Double")
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.daq_set_port("test1", daq_handle, 1, "Expression_1", "y[0]",
                             mrt_port_type_t.MRT_OUTPUT_PORT, "Double")
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.start_daq("test1", daq_handle)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    #ec = my_mrt.daq_clear_port("test1", daq_handle, 0)
    #assert ec.value == 0

    #ec = my_mrt.daq_clear_all_ports("test1", daq_handle)
    #assert ec.value == 0

    #ec = my_mrt.daq_set_port("test1", daq_handle, 0, "Expression_1", "x[0]",
                             #mrt_port_type_t.MRT_INPUT_PORT)
    #assert ec.value == 0, "resValue:{}".format(ec.value)


    ec, port_info = my_mrt.get_port_info("test1", daq_handle, 0, "Expression_1", "x[0]", "InputPort")
    assert ec.value == 0, "resValue:{}".format(ec.value)

    #ec = my_mrt.daq_append_trigger_event("test1", daq_handle, "hahah", "timeout")
    # assert ec.value == 0, "resValue:{}".format(ec.value)

    #ec, evinfo = my_mrt.daq_get_trigger_event("test1", daq_handle, 1, "Expression_1", "timeout")
    # assert ec.value == 0, "resValue:{}".format(ec.value)

    #ec = my_mrt.daq_remove_trigger_event("test1", daq_handle, "hahah", "timeout")
    # assert ec.value == 0, "resValue:{}".format(ec.value)

    #ec = my_mrt.daq_clear_trigger_events("test1", daq_handle)
    # assert ec.value == 0, "resValue:{}".format(ec.value)


    time.sleep(5)

    #rc = my_mrt.set_input_port_value("test1", "Expression_1", "x[0]", "Double", 1.1)
    #assert rc == 8


    res_code  = my_mrt.daq_read("test1", daq_handle,item_count=1,sub_struct_detail=None)

    # assert res_code == 50, "resValue:{}".format(ec.value)

    # ec = my_mrt.daq_msg_release(daq_handle)
    # assert rc == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.stop_daq("test1", daq_handle)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    ec = my_mrt.destroy_daq("test1", daq_handle)
    assert ec.value == 0, "resValue:{}".format(ec.value)

    # ec = my_mrt.stop_test("test1")
    # assert ec.value == 0
    # ec = my_mrt.delete_test_env("test1")
    # assert ec.value == 0
    # ec, num = my_mrt.get_env_number()
    # assert ec.value == 0
    # assert num == 0
    print("haha")
