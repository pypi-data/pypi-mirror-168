from kunyi_hil_test import *
from kunyi_mrt import *
from kunyi_daq_monitor import *

my_mrt = mrt_client("192.168.5.18", "8888", "8889", "8890")
ec = my_mrt.connet()
env_name = "187aa472a59443009643ebbd2af5c996"

rc, value = my_mrt.get_input_port_value(env_name, "Expression_3", "x[0]", "Double",item_count=1)
rc, valuey = my_mrt.get_output_port_value(env_name, "Expression_3", "y[0]", "Double",item_count=1)
print("aa")