'''
    *************************************************************
    *                   DirectoryManager.py                     *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import os

# ----------------------------
# Setting some constant values
# ----------------------------

# below, the generilized sub-directory of the plc file is listed
path2_dh_DT = 'cif_plc_control'
test_names = ["test1a", "test1b", "test2", "test3a", "test3b"]

# ---------------------------------------------
# Funtions to add required folders to directory
# ---------------------------------------------

# adding sub-directories for the different scratch videos of the different tests
def scratchVidNames(test_names, dir_scratch):
    names = []
    dir_scratch = dir_scratch
    for test in test_names:
        names.append(os.path.join(dir_scratch, test + ".avi"))
    return names

# adding a folder for the grading files to be put into
def gradeFolder():
    dir_grades = "grades"
    if not os.path.exists(dir_grades):
        os.makedirs(dir_grades)


