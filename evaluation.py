import os
import subprocess
import time

import pandas as pd
import numpy as np


# test_list = []
ctr = 1
for dirs, subdirs, files in os.walk(".\\Eval"):
#     start_time = time.time()
    for file in files:
        test_path = os.path.join(dirs,file)
        exe_cmd = "python Scripts\cbs_main.py -i %s -o 25 -b out\\benchmark_all.csv"%(test_path)
#         current_time = time.time()
        print(exe_cmd)
        print("####################################################")
        print(ctr)
        print("####################################################")       
#         test_list.append(1)
        subprocess.run(exe_cmd)
        ctr += 1
# print(np.asarray(test_list).sum())

