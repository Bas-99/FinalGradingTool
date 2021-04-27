'''
    *************************************************************
    *                       TestExecuter.py                     *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import os

# ----------------------------------------------------
# Importing variables and functions from other Modules
# ----------------------------------------------------

from TestFunctions import test_list
from TestFunctions import time_test1a, time_test1b, time_test2, time_test3a, time_test3b
from Recorder import screenRec, frameFilter
from ProgramExecuter import appRunner, appCloser
from DirectoryManager import scratchVidNames

# ------------------------------------
# Definition of test executer function
# ------------------------------------

def testExecuter(save_path_filtered, fps, fourcc_avi, folder_dh_DT, assignment, path_unity,
                 path_TwinCat, test_names, dir_scratch):

    names = scratchVidNames(test_names, dir_scratch)
    # defining recording time
    sim_time = [time_test1a, time_test1b, time_test2, time_test3a, time_test3b]

    # video specifications
    widths = [124, 124, 204, 148, 96]
    heights = [138, 138, 46, 175, 122]

    sizes = [(widths[0], heights[0]), (widths[1], heights[1]),
             (widths[2], heights[2]), (widths[3], heights[3]),
             (widths[4], heights[4])]

    ofsets_h = [431, 431, 266, 1254, 1388]
    ofsets_v = [99, 99, 190, 232, 231]

    count = 0
    for current_test in test_list:
        if count >= len(test_names):
            break

        appRunner(path_unity, path_TwinCat, folder_dh_DT)

        current_test()

        screenRec(fps, sim_time[count], fourcc_avi, names[count],
                  widths[count], heights[count], sizes[count],
                  ofsets_h[count], ofsets_v[count])

        appCloser()
        dir_vid = os.path.join(save_path_filtered, test_names[count])
        frameFilter(names[count], fps, heights[count],
                    widths[count], dir_vid, fourcc_avi, test_names[count], assignment)
        count += 1