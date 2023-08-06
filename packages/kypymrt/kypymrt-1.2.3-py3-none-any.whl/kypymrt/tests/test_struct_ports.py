import os.path
import time

from kunyi_mrt import *
from kunyi_project import hil_project


def test_struct_port():
    struct_project = hil_project(r'C:\Users\windy\Documents\IntegratePortal0829\.ip\Build\IntegratePortal0829.ipr')
    # struct_project = hil_project(r'D:\work\EE\pymrt\CANIP\IntegratePortal0829\.ip\Build\IntegratePortal0829.ipr')
    input_port_meta = struct_project.get_instance_item("VectorCAN_1", "Inport", "InputPorts")
    input_port_struct = struct_project.get_instance_item("VectorCAN_1", input_port_meta["RefStruct"], "Structs")
    all_structs = struct_project.get_instance_items("VectorCAN_1", "Structs")

    env_name = "can_input"
    my_mrt = mrt_client("127.0.0.1", "8888", "8889", "8890")
    ec = my_mrt.connet()
    assert ec.value == 0
    ec = my_mrt.create_test_env(env_name)
    assert ec.value == 0

    ec, name = my_mrt.get_env_name_by_idx(0)
    assert ec.value == 0
    assert name == env_name

    ec, num = my_mrt.get_env_number()
    assert ec.value == 0
    assert num == 1
    # pf_path = os.path.abspath(r'C:\Users\windy\Documents\IntegratePortal0829\.ip\Build\Packages.zip')
    pf_path = os.path.abspath(r'D:\work\EE\pymrt\CANIP\IntegratePortal0829\.ip\Build\Packages.zip')

    ec, file_id = my_mrt.download_file(pf_path)
    assert ec.value == 0
    time.sleep(1)
    while True:
        value = mrt_client.dispatch_progress
        if value >= 1:
            break

    assert value == 1

    my_mrt.load_test_resources_to_env(env_name, file_id)

    ec = my_mrt.start_test(env_name)
    assert ec.value == 0
    ec, info = my_mrt.get_env_info(env_name)
    assert info.contents.running_status == 1

    can_data = {"id": 999,
                "name": [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9],
                "protocol_mode": 0,
                "is_extended": 1,
                "timestamp": 1661841709,
                "length": 11,
                "dlc": 8,
                "data": [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                         9, 9, 9, 9],
                "is_error": 0,
                "is_remote": 0,
                "esi": 0,
                "brs": 500000
                }

    rc = my_mrt.set_input_port_value(env_name, "VectorCAN_1", "Inport", "Struct", can_data, 1, input_port_struct,
                                     **all_structs)

    rc, value = my_mrt.get_input_port_value(env_name, "VectorCAN_1", "Inport", "Struct", 1, input_port_struct,
                                            **all_structs)
    print("**")
