'''
    *************************************************************
    *                   SavingLoading.py                        *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import json

# ------------------
# Save and Load Data
# ------------------

def saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models):
    dirs = [general_path, path_TwinCat, path_unity, dir_assignments, dir_models]
    with open('savedData.json', 'w') as f:
        json.dump(dirs, f)

def loadDirs():
    f = open('savedData.json')
    data = json.load(f)
    return data

# --------------------
# Save and Load Grades
# --------------------

def saveGrades(sub_scores, final_scores, groups):
    scores = [sub_scores, final_scores, groups]
    with open('savedGrades.json', 'w') as f:
        json.dump(scores, f)

def loadGrades():
    f = open('savedGrades.json')
    scores = json.load(f)
    return scores