from ctypes import *
from Enums import *
mrt_file_id_t = c_uint64
mrt_daq_handle_t = c_uint64
class mrt_enviroment_info_t(Structure):
    _fields_ = [
        ("loaded_file_id", mrt_file_id_t), ("running_status", c_uint32)
    ]

class mrt_daq_info_t(Structure):
    _fields_ = [
        ("port_num", c_uint32), ("trigger_event_num", c_uint32),("period_ms", c_uint32),
        ("offset_ms", c_uint32),("msg_data_size", c_uint32)
    ]

class mrt_daq_trigger_event_info_t(Structure):
    _fields_ = [
        ("model_instance_name", c_char*64), ("event_name",c_char*64)
    ]

class mrt_daq_port_info_t(Structure):
    _fields_ = [
        ("model_instance_name", c_char*64), ("port_name",c_char*64),("port_type_name",c_char*64),
        ("port_type",mrt_port_type_t),("data_type",mrt_port_data_type_t),("data_size",c_uint32),
        ("array_size",c_uint32),("pos_in_daq_data",c_uint32)
    ]

class mrt_daq_msg_t(Structure):
    _fields_ = [("daq",mrt_daq_handle_t),("time_stamp_us",c_uint64),("sn",c_uint32),("data_size",c_uint32),
                ("data", c_void_p)]

