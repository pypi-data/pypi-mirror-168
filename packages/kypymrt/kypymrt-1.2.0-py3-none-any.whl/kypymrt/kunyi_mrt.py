from ctypes import *
from ctypes import wintypes
from kunyi_util import *
from Enums import *
from mrt_strunctures import *
import pathlib
import time

dll_path = os.path.join(pathlib.Path(__file__).parent, "mrt.dll")
mrt_lib = WinDLL(dll_path)


class mrt_client():
    dispatch_progress = 0

    def __init__(self, host, managerment_port=8888, push_port=8889, subscription_port=8890):
        self.host = host
        self.mgr_port = managerment_port
        self.push_port = push_port
        self.subs_port = subscription_port
        self.envs = {}
        self.context = None
        self.daqs = {}
        self.data_listTemp = []
        self.recodeStatus = 0
        self.writeNo = 1

    def connet(self):

        error_code = mrt_status_t()
        p_ec = pointer(error_code)
        con_str = "tcp://%s:%s" % (self.host, self.mgr_port)

        bs = con_str.encode('utf-8')
        con_str_pointer = c_char_p(bs)

        mrt_lib.mrt_create_context.restype = c_void_p
        self.context = mrt_lib.mrt_create_context(con_str_pointer, p_ec)

        return error_code

    def disconnect(self):
        if self.context == None:
            return 0
        mrt_lib.mrt_destroy_context.argtypes = [c_void_p]
        mrt_lib.mrt_destroy_context.restype = mrt_status_t
        error_code = mrt_lib.mrt_destroy_context(self.context)
        if error_code == 0:
            self.context = None
        return error_code

    def create_test_env(self, env_name):
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        mrt_lib.mrt_create_enviroment.argtypes = [c_void_p, c_char_p]
        mrt_lib.mrt_create_enviroment.restype = mrt_status_t
        error_code = mrt_lib.mrt_create_enviroment(self.context, name_pointer)
        if error_code.value == 0:
            self.envs[env_name] = None
        return error_code

    def delete_test_env(self, env_name):
        # if env_name not in self.envs:
        #    return mrt_status_t.MRT_ERR_OBJECT_NOT_EXIST
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        mrt_lib.mrt_destroy_enviroment.argtypes = [c_void_p, c_char_p]
        mrt_lib.mrt_destroy_enviroment.restype = mrt_status_t
        error_code = mrt_lib.mrt_destroy_enviroment(self.context, name_pointer)
        if error_code.value == 0:
            try:
                del self.envs[env_name]
            except:
                pass
        return error_code

    def load_test_resources_to_env(self, env_name, fileid):
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        mrt_lib.mrt_load_enviroment.argtypes = [c_void_p, c_char_p, POINTER(c_uint64)]
        mrt_lib.mrt_load_enviroment.restype = mrt_status_t
        error_code = mrt_lib.mrt_load_enviroment(self.context, name_pointer, byref(c_uint64(fileid)))
        return error_code

    def start_test(self, env_name):
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        mrt_lib.mrt_start_enviroment.argtypes = [c_void_p, c_char_p]
        mrt_lib.mrt_start_enviroment.restype = mrt_status_t
        error_code = mrt_lib.mrt_start_enviroment(self.context, name_pointer)

        return error_code

    def stop_test(self, env_name):
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        mrt_lib.mrt_stop_enviroment.argtypes = [c_void_p, c_char_p]
        mrt_lib.mrt_stop_enviroment.restype = mrt_status_t
        error_code = mrt_lib.mrt_stop_enviroment(self.context, name_pointer)
        return error_code

    def get_env_number(self):
        num_pointer = pointer(c_int())
        mrt_lib.mrt_get_enviroment_number.argtypes = [c_void_p, c_void_p]
        mrt_lib.mrt_get_enviroment_number.restype = mrt_status_t
        error_code = mrt_lib.mrt_get_enviroment_number(self.context, num_pointer)
        return error_code, num_pointer.contents.value

    def _rebuild_self_env_dict(self, real_env_num):
        for i in range(real_env_num):
            pass

    def get_env_info(self, env_name):
        bs = env_name.encode('utf-8')
        name_pointer = c_char_p(bs)
        info = mrt_enviroment_info_t()
        ei_p = pointer(info)
        mrt_lib.mrt_get_enviroment_info.argtypes = [c_void_p, c_char_p, POINTER(mrt_enviroment_info_t)]
        mrt_lib.mrt_get_enviroment_info.restype = mrt_status_t
        error_code = mrt_lib.mrt_get_enviroment_info(self.context, name_pointer, byref(info))
        return error_code, ei_p

    def get_env_name_by_idx(self, idx):
        ec, num = self.get_env_number()
        if ec.value != 0:
            return None
        # if idx >= num:
        #    return None

        arr = bytearray(512)
        char_array = c_char * len(arr)
        buf_c = char_array.from_buffer(arr)
        size_pointer = pointer(c_int32(512))
        mrt_lib.mrt_get_enviroment_name.argtypes = [c_void_p, c_uint32, c_char_p, POINTER(c_int32)]
        mrt_lib.mrt_get_enviroment_name.restype = mrt_status_t
        error_code = mrt_lib.mrt_get_enviroment_name(self.context, idx, buf_c, size_pointer)
        return error_code, buf_c.value.decode('utf-8')

    @staticmethod
    def call_back(error_code, current_process, total_process):
        if error_code.value != 0:
            mrt_client.dispatch_progress = 100
        mrt_client.dispatch_progress = float(current_process) / float(total_process)

    def download_file(self, file_path):
        bs = file_path.encode('utf-8')
        path_pointer = c_char_p(bs)
        file_id_pointer = pointer(c_uint64())
        CALLBACK = CFUNCTYPE(None, mrt_status_t, c_int, c_int)
        mrt_lib.mrt_download_file.argtypes = [c_void_p, c_char_p, CALLBACK, POINTER(c_uint64)]
        mrt_lib.mrt_download_file.restype = mrt_status_t
        my_callback = CALLBACK(mrt_client.call_back)
        error_code = mrt_lib.mrt_download_file(self.context, path_pointer, my_callback, file_id_pointer)
        return error_code, file_id_pointer.contents.value

    def get_env_file_id(self, env_name):
        pass

    def list_envs(self):
        pass

    def list_running_env(self):
        pass

    def get_test_env_detail(self):
        pass

    def dump_test_env(self):
        pass

    def get_input_port_value(self, env_name, instance_name, port_name, signal_type, item_count, struct_detail=None, **sub_struct_detail):
        return self.get_port_value(env_name, instance_name, port_name,
                                   signal_type, mrt_port_type_t.MRT_INPUT_PORT, item_count, struct_detail, **sub_struct_detail)

    def get_output_port_value(self, env_name, instance_name, port_name, signal_type, item_count, struct_detail=None, **sub_struct_detail):
        return self.get_port_value(env_name, instance_name, port_name,
                                   signal_type, mrt_port_type_t.MRT_OUTPUT_PORT, item_count, struct_detail, **sub_struct_detail)

    def get_measurement_value(self, env_name, instance_name, port_name, signal_type, item_count, struct_detail=None, **sub_struct_detail):
        return self.get_port_value(env_name, instance_name, port_name,
                                   signal_type, mrt_port_type_t.MRT_MEASUREMENT, item_count, struct_detail, **sub_struct_detail)

    def get_port_value(self, env_name, instance_name, port_name, signal_type, port_type, item_count, struct_detail, **sub_struct_detail):
        en_bs = env_name.encode('utf-8')
        en_pointer = c_char_p(en_bs)
        in_bs = instance_name.encode('utf-8')
        in_pointer = c_char_p(in_bs)
        pn_bs = port_name.encode('utf-8')
        pn_pointer = c_char_p(pn_bs)

        buf_size = kunyi_util.get_signal_bytes_length(signal_type, item_count, struct_detail, **sub_struct_detail)
        if buf_size == None:
            return mrt_status_t.MRT_ERR_INVALID_ARG, None

        arr = bytearray(buf_size)
        char_array = c_char * len(arr)
        buf_c = char_array.from_buffer(arr)

        mrt_lib.mrt_model_read_port.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p,
                                                c_int32, c_int32, c_int32, c_void_p]
        mrt_lib.mrt_model_read_port.restype = c_int32
        return_bytes = mrt_lib.mrt_model_read_port(self.context, en_pointer, in_pointer, pn_pointer,
                                                 port_type[0], 0, buf_size, buf_c)
        port_value = kunyi_util.bytes_to_data(signal_type, arr, item_count, struct_detail, **sub_struct_detail)
        return return_bytes, port_value

    def set_input_port_value(self, env_name, instance_name, port_name, signal_type, signal_value,
                             item_count, struct_detail, **sub_struct_detail):
        return self.set_port_value(env_name, instance_name, port_name,
                                   signal_type, signal_value, mrt_port_type_t.MRT_INPUT_PORT,
                                   item_count, struct_detail, **sub_struct_detail)

    def set_port_value(self, env_name, instance_name, port_name, signal_type, signal_value,
                       port_type, item_count, struct_detail, **sub_struct_detail):
        en_bs = env_name.encode('utf-8')
        en_pointer = c_char_p(en_bs)
        in_bs = instance_name.encode('utf-8')
        in_pointer = c_char_p(in_bs)
        pn_bs = port_name.encode('utf-8')
        pn_pointer = c_char_p(pn_bs)

        python_bytes = kunyi_util.data_to_bytes(signal_type, signal_value, item_count,
                                                struct_detail, **sub_struct_detail)
        arr = bytearray.fromhex(python_bytes.hex())
        char_array = c_char * len(arr)
        buf_c = char_array.from_buffer(arr)

        buf_size = kunyi_util.get_signal_bytes_length(signal_type, item_count,
                                                      struct_detail, **sub_struct_detail)
        if buf_size == None:
            return mrt_status_t.MRT_ERR_INVALID_ARG, None

        mrt_lib.mrt_model_write_port.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p,
                                                 c_int32, c_int32, c_int32, c_void_p]
        mrt_lib.mrt_model_write_port.restype = c_int32
        rc = mrt_lib.mrt_model_write_port(self.context, en_pointer, in_pointer, pn_pointer,
                                          port_type[0], 0, buf_size, buf_c)
        return rc

    def get_calibration_value(self, env_name, instance_name, cal_name, axis_idx,
                              data_idx, array_size, cal_datatype):
        en_bs = env_name.encode('utf-8')
        en_pointer = c_char_p(en_bs)
        in_bs = instance_name.encode('utf-8')
        in_pointer = c_char_p(in_bs)
        cn_bs = cal_name.encode('utf-8')
        cn_pointer = c_char_p(cn_bs)

        signal_buf_size = kunyi_util.get_signal_bytes_length(cal_datatype)
        buf_size = array_size * signal_buf_size
        arr = bytearray(buf_size)
        char_array = c_char * len(arr)
        buf_c = char_array.from_buffer(arr)
        mrt_lib.mrt_model_cal_read.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p,
                                                c_int32, c_int32, c_int32, c_void_p]
        mrt_lib.mrt_model_cal_read.restype = c_int32
        error_code = mrt_lib.mrt_model_cal_read(self.context, en_pointer, in_pointer, cn_pointer,
                                                axis_idx, data_idx, buf_size, buf_c)
        if error_code.value != 0:
            return None
        cal_values = kunyi_util.bytes_array_to_data_array(cal_datatype, buf_size, buf_c.value, array_size)

        return cal_values

    def create_daq(self, env_name, port_number, is_queue):
        if is_queue == 1:
            if port_number > 1:
                raise Exception("One daq can only contain one queue port")

        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        daq_handle = pointer(c_uint64())
        mrt_lib.mrt_create_daq.argtypes = [c_void_p, c_char_p, c_int32, POINTER(c_uint64), c_int]
        mrt_lib.mrt_create_daq.restype = mrt_status_t
        error_code = mrt_lib.mrt_create_daq(self.context, en_pointer, port_number, daq_handle, is_queue)
        if error_code.value == 0:
            self.daqs[daq_handle.contents.value] = [None] * port_number
            with open("./daqinfo.txt","w") as f:
                f.write(str(daq_handle.contents.value))
        return error_code, daq_handle.contents.value

    def destroy_daq(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_destroy_daq.argtypes = [c_void_p, c_char_p, c_uint64]
        mrt_lib.mrt_destroy_daq.restype = mrt_status_t
        error_code = mrt_lib.mrt_destroy_daq(self.context, en_pointer, c_uint64(daq_handle))
        if error_code.value == 0:
            try:
                del(self.daqs[daq_handle])
            except:
                pass
        return error_code

    def get_daq_info(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        daq_info = mrt_daq_info_t()
        inof_p = pointer(daq_info)
        mrt_lib.mrt_get_daq_info.argtypes = [c_void_p, c_char_p, c_uint64, POINTER(mrt_daq_info_t)]
        mrt_lib.mrt_get_daq_info.restype = mrt_status_t
        error_code = mrt_lib.mrt_get_daq_info(self.context, en_pointer, c_uint64(daq_handle), byref(daq_info))
        return error_code, inof_p

    def get_port_info(self, env_name, daq_handle,port_index,model_instance_name,port_name,port_type_name):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        modelName = model_instance_name.encode('utf-8')
        portName = port_name.encode('utf-8')
        portTName = port_type_name.encode('utf-8')
        port_info = mrt_daq_port_info_t(modelName,portName,portTName,mrt_port_type_t.MRT_INPUT_PORT[0],
                                        mrt_port_data_type_t.MRT_DATA_TYPE_FLOAT64[0],10,8,8)
        # port_info = mrt_daq_port_info_t()
        info_p = pointer(port_info)
        mrt_lib.mrt_get_port_info.argtypes = [c_void_p, c_char_p, c_uint64,c_uint32,POINTER(mrt_daq_port_info_t)]
        mrt_lib.mrt_get_port_info.restype = mrt_status_t
        error_code = mrt_lib.mrt_get_port_info(self.context,en_pointer,c_uint64(daq_handle),c_uint32(port_index),byref(port_info))
        return  error_code , info_p


    def daq_set_trigger_period(self, env_name, daq_handle, period_ms, offset_ms):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_daq_set_trigger_period.argtypes = [c_void_p, c_char_p, c_uint64, c_uint32, c_uint32]
        mrt_lib.mrt_daq_set_trigger_period.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_set_trigger_period(self.context, en_pointer, c_uint64(daq_handle),
                                                        period_ms, offset_ms)
        return error_code

    def daq_set_port(self, env_name, daq_handle, port_index, model_instance_name, port_name, port_type, port_datatype):

        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        modelName = model_instance_name.encode('utf-8')
        mn_pointer = c_char_p(modelName)
        portName = port_name.encode('utf-8')
        pn_pointer = c_char_p(portName)
        mrt_lib.mrt_daq_set_port.argtypes = [c_void_p, c_char_p, c_uint64, c_uint32, c_char_p, c_char_p, c_int32]
        mrt_lib.mrt_daq_set_port.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_set_port(self.context, en_pointer, c_uint64(daq_handle), c_uint32(port_index),
                                              mn_pointer, pn_pointer, port_type[0])
        if error_code.value == 0:
            self.daqs[daq_handle][port_index] = (model_instance_name, port_name, port_type[0], port_datatype)
        return error_code

    def daq_clear_port(self, env_name, daq_handle, port_index):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_daq_clear_port.argtypes = [c_void_p, c_char_p, c_uint64, c_uint32]
        mrt_lib.mrt_daq_clear_port.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_clear_port(self.context, en_pointer, c_uint64(daq_handle), c_uint32(port_index))
        if error_code == 0:
            self.daqs[daq_handle][port_index] = None
        return error_code

    def daq_clear_all_ports(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_daq_clear_all_ports.argtypes = [c_void_p, c_char_p, c_uint64]
        mrt_lib.mrt_daq_clear_all_ports.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_clear_all_ports(self.context, en_pointer, c_uint64(daq_handle))
        if error_code == 0:
            for i in range(len(self.daqs[daq_handle])):
                self.daqs[daq_handle][i] = None
        return error_code

    def daq_append_trigger_event(self, env_name, daq_handle, model_instance_name, event_name):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        modelName = model_instance_name.encode('utf-8')
        mn_pointer = c_char_p(modelName)
        eventName = event_name.encode('utf-8')
        eventn_pointer = c_char_p(eventName)
        mrt_lib.mrt_daq_append_trigger_event.argtypes = [c_void_p, c_char_p, c_uint64, c_char_p, c_char_p]
        mrt_lib.mrt_daq_append_trigger_event.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_append_trigger_event(self.context, en_pointer, c_uint64(daq_handle),
                                                          mn_pointer, eventn_pointer)
        return error_code

    def daq_remove_trigger_event(self, env_name, daq_handle, model_instance_name, event_name):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        modelName = model_instance_name.encode('utf-8')
        mn_pointer = c_char_p(modelName)
        eventName = event_name.encode('utf-8')
        eventn_pointer = c_char_p(eventName)
        mrt_lib.mrt_daq_remove_trigger_event.argtypes = [c_void_p, c_char_p, c_uint64, c_char_p, c_char_p]
        mrt_lib.mrt_daq_remove_trigger_event.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_remove_trigger_event(self.context, en_pointer, c_uint64(daq_handle),
                                                          mn_pointer, eventn_pointer)
        return error_code

    def daq_clear_trigger_events(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_daq_clear_trigger_events.argtypes = [c_void_p, c_char_p, c_uint64]
        mrt_lib.mrt_daq_clear_trigger_events.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_clear_trigger_events(self.context, en_pointer, c_uint64(daq_handle))
        return error_code

    def daq_get_trigger_event(self, env_name, daq_handle, port_index, model_instance_name, event_name):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        modelName = model_instance_name.encode('utf-8')
        # mn_pointer = c_char(modelName)
        eventName = event_name.encode('utf-8')
        # eventn_pointer = c_char(eventName)
        evinfo = mrt_daq_trigger_event_info_t(modelName, eventName)
        evinfo_p = pointer(evinfo)
        mrt_lib.mrt_daq_get_trigger_event.argtypes = [c_void_p, c_char_p, c_uint64, c_uint32,
                                                      POINTER(mrt_daq_trigger_event_info_t)]
        mrt_lib.mrt_daq_get_trigger_event.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_get_trigger_event(self.context, en_pointer, c_uint64(daq_handle),
                                                       c_uint32(port_index), byref(evinfo))
        return error_code, evinfo_p

    def start_daq(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_start_daq.argtypes = [c_void_p, c_char_p, c_uint64]
        mrt_lib.mrt_start_daq.restype = mrt_status_t
        error_code = mrt_lib.mrt_start_daq(self.context, en_pointer, c_uint64(daq_handle))
        return error_code


    def open_log_reader(self):
        addr = "tcp://" + self.host + ":" + str(self.subs_port)
        addr_bs = addr.encode('utf-8')
        addr_pointer = c_char_p(addr_bs)

        mrt_lib.mrt_log_reader_open.argtypes = [c_char_p]
        mrt_lib.mrt_log_reader_open.restype = c_void_p
        self.log_reader = mrt_lib.mrt_log_reader_open(addr_pointer)
        return self.log_reader

    def open_log_writter(self):
        addr = "tcp://" + self.host + ":" + str(self.push_port)
        addr_bs = addr.encode('utf-8')
        addr_pointer = c_char_p(addr_bs)

        mrt_lib.mrt_log_writer_open.argtypes = [c_char_p]
        mrt_lib.mrt_log_writer_open.restype = c_void_p
        self.log_writter = mrt_lib.mrt_log_writer_open(addr_pointer)
        return self.log_writter


    def close_log_reader(self):

        mrt_lib.mrt_log_reader_close.argtypes = [c_void_p]
        mrt_lib.mrt_log_reader_close.restype = mrt_status_t
        ec = mrt_lib.mrt_log_reader_close(self.log_reader)
        if ec.value == 0:
            self.log_reader = None
        return ec

    def close_log_writter(self):

        mrt_lib.mrt_log_writer_close.argtypes = [c_void_p]
        mrt_lib.mrt_log_writer_close.restype = mrt_status_t
        ec = mrt_lib.mrt_log_writer_close(self.log_writter)
        if ec.value == 0:
            self.log_writter = None
        return ec

    def fetch_log(self, buf_size):
        arr = bytearray(buf_size)
        char_array = c_char * len(arr)
        buf_c = char_array.from_buffer(arr)

        mrt_lib.mrt_log_read.argtypes = [c_void_p, c_char_p, c_int32, c_int32]
        mrt_lib.mrt_log_read.restype = c_int32
        size = mrt_lib.mrt_log_read(self.log_reader, buf_c, buf_size, 5)
        log_data = kunyi_util.bytes_to_data("UTF8", arr[:size])
        return log_data

    def stop_daq(self, env_name, daq_handle):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        mrt_lib.mrt_stop_daq.argtypes = [c_void_p, c_char_p, c_uint64]
        mrt_lib.mrt_stop_daq.restype = mrt_status_t
        error_code = mrt_lib.mrt_stop_daq(self.context, en_pointer, c_uint64(daq_handle))
        return error_code

    def daq_read(self, env_name, daq_handle, item_count, sub_struct_detail):
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        msg_pp = pointer(c_void_p())
        is_release = False
        msg_list = []
        try:
            mrt_lib.mrt_daq_read.argtypes = [c_void_p, c_char_p, c_uint64, POINTER(POINTER(None))]
            mrt_lib.mrt_daq_read.restype = c_int32
            buf_size = mrt_lib.mrt_daq_read(self.context, en_pointer, c_uint64(daq_handle), msg_pp)
            if buf_size == 0:
                print(f"The experimental environment is not running:{buf_size}")
                return msg_list
            elif buf_size == -6:
                raise Exception("MRT_ERR_RPC_CALL_FAIL")
            elif buf_size < 0:
                raise Exception(f"Experiment environment error code:{buf_size}")
            mrt_msg_array = mrt_daq_msg_t * buf_size
            msg_arr_obj = mrt_msg_array.from_address(msg_pp.contents.value)
            if msg_arr_obj:
                is_release = True

            ports = self.daqs[daq_handle]
            for msg in msg_arr_obj:
                data_buf = c_char * msg.data_size
                data_byte_arr = data_buf.from_address(msg.data)
                data_pba = bytearray(data_byte_arr)
                p_idx = 0
                buf_read_idx = 0
                data_list = []
                for item in ports:
                    if item is None:
                        continue
                    item_size = kunyi_util.get_signal_bytes_length(item[3],item_count,sub_struct_detail)
                    item_data_buf = data_pba[buf_read_idx: buf_read_idx+item_size]
                    item_data_value = kunyi_util.bytes_to_data(item[3], item_data_buf,item_count,sub_struct_detail)
                    data_list.append((item[0], item[1], item[2], item_data_value, msg.time_stamp_us))
                    buf_read_idx = buf_read_idx + item_size
                    p_idx = p_idx + 1
                msg_list.append(data_list)
            return msg_list
        except Exception as ex:
            raise ex
        finally:
            if is_release:
                releaseInfo = self.daq_msg_release(msg_arr_obj[0])
                if releaseInfo.value != 0:
                    raise Exception("rtcp error after read daq data")

    def daq_write_temp(self, env_name, daq_handle,item_count,struct_detail=None,isTrigger = False,
                       trigger_start=None,trigger_stop=None):
        with open(f"./infoFile/PortMsg.txt", "w") as f:
            f.write(str(self.daqs))
        bs = env_name.encode('utf-8')
        en_pointer = c_char_p(bs)
        msg_pp = pointer(c_void_p())
        fileNum = 1
        is_release = False
        try:
            mrt_lib.mrt_daq_read.argtypes = [c_void_p, c_char_p, c_uint64, POINTER(POINTER(None))]
            mrt_lib.mrt_daq_read.restype = c_int32
            buf_size = mrt_lib.mrt_daq_read(self.context, en_pointer, c_uint64(daq_handle), msg_pp)
            if buf_size == 0:
                print(f"The experimental environment is not running:{buf_size}")
                return None
            elif buf_size ==-6:
                print(f"The experimental environment has been destroyed code:{buf_size}")
                return None
            elif buf_size < 0:
                print(f"Experiment environment error code:{buf_size}")
                return None
            mrt_msg_array = mrt_daq_msg_t * buf_size
            msg_arr_obj = mrt_msg_array.from_address(msg_pp.contents.value)
            if msg_arr_obj:
                is_release = True
            with open(f"./dataRecordTemp/dataRecord_{fileNum}.tmp", "ab") as f:
                ports = self.daqs[daq_handle]
                for msg in msg_arr_obj:
                    data_buf = c_char * msg.data_size
                    data_byte_arr = data_buf.from_address(msg.data)
                    data_pba = bytearray(data_byte_arr)
                    buf_read_idx = 0
                    data_list = []
                    for item in ports:
                        if item is None:
                            continue
                        item_size = kunyi_util.get_signal_bytes_length(item[3], item_count, struct_detail)
                        item_data_buf = data_pba[buf_read_idx: buf_read_idx + item_size]
                        item_data_value = kunyi_util.bytes_to_data(item[3], item_data_buf, item_count,
                                                                   struct_detail)
                        data_list.append((item[0], item[1], item[2], item_data_value, msg.time_stamp_us))
                        buf_read_idx = buf_read_idx + item_size
                    self.data_listTemp = data_list
                    t=msg.time_stamp_us
                    t_bytes = kunyi_util.data_to_bytes("UInt64",t,1,struct_detail=None)
                    if isTrigger:
                        tri_start = self.record_trigger_start(*trigger_start)
                        tri_stop =  self.record_trigger_stop(*trigger_stop)
                        if tri_start and not tri_stop:
                            if self.recodeStatus < 0:
                                self.recodeStatus = 0
                            self.recodeStatus +=1
                            if self.recodeStatus == 1:
                                print("Start the trigger!")
                            f.write(t_bytes+data_pba)
                            print(f"\rWrite to successful No:{self.writeNo}!",end='')
                            self.writeNo +=1
                        else:
                            if self.recodeStatus > 0:
                                self.recodeStatus = 0
                            if self.recodeStatus == 0:
                                print("\nstop-record!")
                                self.recodeStatus -= 1
                            continue
                    else:
                        f.write(t_bytes + data_pba)
                        print(f"\rWrite to successful No:{self.writeNo}!", end='')
                        self.writeNo += 1
                    f.flush()
                    statinfo = os.stat(f"./dataRecordTemp/dataRecord_{fileNum}.tmp")
                    if statinfo.st_size >= 1073741824:  # 1M
                        fileNum += 1
        except Exception as ex:
            raise ex
        finally:
            if is_release:
                releaseInfo = self.daq_msg_release(msg_arr_obj[0])
                if releaseInfo.value != 0:
                    raise Exception("rtcp error after read daq data")

    def daq_msg_release(self, msg):

        mrt_lib.mrt_daq_msg_release.argtypes = [c_void_p, POINTER(mrt_daq_msg_t)]
        mrt_lib.mrt_daq_msg_release.restype = mrt_status_t
        error_code = mrt_lib.mrt_daq_msg_release(self.context, msg)
        return error_code

    def record_trigger(self,instance_name, port_name, trigger_mode,signal_value,signal_value2=None):
        for portData in self.data_listTemp:
            if portData[0]== instance_name and portData[1].decode('utf-8') ==port_name:
                if trigger_mode == "=" and portData[3]== signal_value:
                    return True
                if trigger_mode == "!=" and portData[3] != signal_value:
                    return True
                if trigger_mode == ">" and portData[3] >signal_value:
                    return True
                if trigger_mode == "<" and portData[3] <signal_value:
                    return True
                if trigger_mode == ">=" and portData[3] >= signal_value:
                    return True
                if trigger_mode == "<=" and portData[3] <= signal_value:
                    return True
                if trigger_mode == "between" and signal_value <= portData[3] <= signal_value2:
                    return True
                else:
                    continue

    def record_trigger_start(self,instance_name, port_name, trigger_mode,signal_value,signal_value2=None):
        if self.record_trigger(instance_name, port_name, trigger_mode,signal_value,signal_value2):
            return True

    def record_trigger_stop(self,instance_name, port_name, trigger_mode,signal_value,signal_value2=None):
        if self.record_trigger(instance_name, port_name, trigger_mode, signal_value, signal_value2):
            return True

