'''
    *************************************************************
    *                  SimulationExecuter.py                    *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import cv2
import time
import os

# ----------------------------------------------------
# Importing variables and functions from other Modules
# ----------------------------------------------------

from DirectoryManager import path2_dh_DT
from TestExecuter import testExecuter

# ----------------------------
# Simulation Executer Function
# ----------------------------

def simulationExecuter(dir_simulations, dir_assignments,assignments, path_unity,
                       path_TwinCat, test_names, dir_scratch):

    # defining frame rate
    fps = 10.0

    # defining the codec
    fourcc_avi = cv2.VideoWriter_fourcc(*"XVID")

    total_start = time.time()

    # looping over all assignments
    for i in range(len(assignments)):
        as_start = time.time()
        folder_dh_DT = os.path.join(dir_assignments, assignments[i], path2_dh_DT)
        # running the testExecuter() function for every assignment
        testExecuter(dir_simulations, fps, fourcc_avi, folder_dh_DT, assignments[i],
                     path_unity, path_TwinCat, test_names, dir_scratch)
        as_end = time.time()
        as_duration = as_end - as_start
        print("Performing all tests on " + assignments[i] + " took: " + str(as_duration) + " seconds")

    total_end = time.time()
    total_duration = total_end - total_start
    print("All assingments were analyzed in: " + str(total_duration / 60) + " minutes")
