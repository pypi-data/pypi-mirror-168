from kunyi_util import *
from decimal import Decimal
from pathlib import Path
import os
import glob

class TestUtilFuncs():
    def test_byte_data_exchange(self):
        #test ascii
        test_data = "hahahth140e5!@#*"
        data_type = "ASCII"
        self.do_the_test(data_type, test_data)

        # test utf-8
        test_data = "昆易测试"
        data_type = "UTF8"
        self.do_the_test(data_type, test_data)

        # test int8
        test_data = 127
        data_type = "Int8"
        self.do_the_test(data_type, test_data)

        test_data = -128
        data_type = "Int8"
        self.do_the_test(data_type, test_data)

        # test uint8
        test_data = 254
        data_type = "UInt8"
        self.do_the_test(data_type, test_data)

        # test int16
        test_data = -32768
        data_type = "Int16"
        self.do_the_test(data_type, test_data)

        test_data = 32767
        data_type = "Int16"
        self.do_the_test(data_type, test_data)

        # test uint16
        test_data = 65535
        data_type = "UInt16"
        self.do_the_test(data_type, test_data)

        # test int32
        test_data = -2147483648
        data_type = "Int32"
        self.do_the_test(data_type, test_data)
        test_data = 2147483647
        data_type = "Int32"
        self.do_the_test(data_type, test_data)

        # test uint32
        test_data = 4294967295
        data_type = "UInt32"
        self.do_the_test(data_type, test_data)

        # test int64
        test_data = -9223372036854775808
        data_type = "Int64"
        self.do_the_test(data_type, test_data)
        test_data = 9223372036854775807
        data_type = "Int64"
        self.do_the_test(data_type, test_data)

        # test uint64
        test_data = 18446744073709551615
        data_type = "UInt64"
        self.do_the_test(data_type, test_data)

        #test float
        bytes_re = kunyi_util.data_to_bytes("Double", 1.7976931348623157e+308)
        data_re = kunyi_util.bytes_to_data("Double", bytes_re)
        assert data_re == 1.7976931348623157e+308

    def do_the_test(self, type, data):
        bytes_re = kunyi_util.data_to_bytes(type, data, 1)
        data_re = kunyi_util.bytes_to_data(type, bytes_re, 1)
        assert data_re == data

    def test_zip_compress(self):
        root_path = "./ip_projects/Build_folder"

        kunyi_util.file_compress(root_path,  './ip_projects/output/test.zip')

    def test_struct_1(self):
        data = {"id":123}
        struct_detail = {"Name" : "test",
                         "Member": [
                             {
                                "ByteOrder" : "LSBFirst",
                                "DisplayName" : "Frame ID",
                                "ItemCount" : 1,
                                "MaxValue" : 255,
                                "MinValue" : 0,
                                "Name" : "id",
                                "RefComputeMethod" : "",
                                "RefStruct" : "",
                                "Type" : "UInt8"
                                }]}
        self.do_test_struct("Struct", data, struct_detail)

    def test_struct_2(self):
        data = {"id": 123,
                "name": [9,9,9,9,9,9,9,9]}
        struct_detail = {"Name": "test",
                         "Member": [
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "Frame ID",
                                 "ItemCount": 1,
                                 "MaxValue": 255,
                                 "MinValue": 0,
                                 "Name": "id",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "name",
                                 "ItemCount": 8,
                                 "MaxValue": 255,
                                 "MinValue": 0,
                                 "Name": "name",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             }
                         ]}
        self.do_test_struct("Struct", data, struct_detail)

    def test_struct_3(self):
        data = {"id": 123,
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
        struct_detail = {"Name": "test",
                         "Member": [
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "Frame ID",
                                 "ItemCount": 1,
                                 "MaxValue": 536870911,
                                 "MinValue": 0,
                                 "Name": "id",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "Name",
                                 "ItemCount": 64,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "name",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "CAN/CANFD",
                                 "ItemCount": 1,
                                 "MaxValue": 1,
                                 "MinValue": 0,
                                 "Name": "protocol_mode",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": 1,
                                 "MinValue": 0,
                                 "Name": "is_extended",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "timestamp",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt64"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "length",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt32"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": 64,
                                 "MinValue": 0,
                                 "Name": "dlc",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 64,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "data",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": 1,
                                 "MinValue": 0,
                                 "Name": "is_error",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": 1,
                                 "MinValue": 0,
                                 "Name": "is_remote",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt8"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "esi",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt32"
                             },
                             {
                                 "ByteOrder": "LSBFirst",
                                 "DisplayName": "",
                                 "ItemCount": 1,
                                 "MaxValue": "",
                                 "MinValue": "",
                                 "Name": "brs",
                                 "RefComputeMethod": "",
                                 "RefStruct": "",
                                 "Type": "UInt32"
                             }
                         ]}
        self.do_test_struct("Struct", data, struct_detail)


    def do_test_struct(self, type, data, struct, **all_structs):
        bytes_re = kunyi_util.data_to_bytes(type, data, 1, struct, **all_structs)
        data_re = kunyi_util.bytes_to_data(type, bytes_re, 1, struct, **all_structs)
        assert len(data) == len(data_re)
        for k,v in data.items():
            assert data[k] == data_re[k]







