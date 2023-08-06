from ctypes import *
from enum import Enum

class enum_base (c_int):
    def get_name(self):
        members= dir(self)
        for m in members:
            v = getattr(self, m)
            if ("MRT_" in m) and (v[0] == self.value):
                return m

class mrt_status_t(enum_base):
    MRT_STS_OK = 0,
    MRT_ERR_INVALID_ARG = -1,
    MRT_ERR_OBJECT_ALREADY_EXIST = -2,
    MRT_ERR_OBJECT_NOT_EXIST = -3,
    MRT_ERR_OBJECT_CREATE_FAIL = -4,
    MRT_ERR_CONNECT_FAIL = -5,
    MRT_ERR_RPC_CALL_FAIL = -6,
    MRT_ERR_RPC_SERVICE_NOT_AVAILABLE = -7,
    MRT_ERR_FILE_ID_NOT_MATCH = -8,
    MRT_ERR_RPC_CALL_TIMEOUT = -9,
    MRT_ERR_INVALID_NAME = -10,
    NO_USE = -99


class mrt_port_type_t(enum_base):
    MRT_INPUT_PORT = 0,
    MRT_OUTPUT_PORT = 1,
    MRT_MEASUREMENT = 2,
    MRT_UNKNOWN_PORT = 3
    NO_USE = -99



class mrt_port_data_type_t(enum_base):
    MRT_DATA_TYPE_UINT8 = 0,
    MRT_DATA_TYPE_UINT16 = 1,
    MRT_DATA_TYPE_UINT32 = 2,
    MRT_DATA_TYPE_UINT64 = 3,
    MRT_DATA_TYPE_INT8 = 4,
    MRT_DATA_TYPE_INT16 = 5,
    MRT_DATA_TYPE_INT32 = 6,
    MRT_DATA_TYPE_INT64 = 7,
    MRT_DATA_TYPE_FLOAT32 = 8,
    MRT_DATA_TYPE_FLOAT64 = 9,
    MRT_DATA_TYPE_STRUCT = 10,
    NO_USE = -99


class fetch_value_type(enum_base):
    ON_DEMAND = 0,
    DAQ = 1,
    NO_USE = -99


class fetch_value_datatype(enum_base):
    RAW = 0,
    PHY = 1,
    NO_USE = -99

