'''
    *************************************************************
    *                   grader_GUI.py                           *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import PySimpleGUI as sg
import numpy as np
import os
import time

# --------------------------------------
# Importing functions from other modules
# --------------------------------------

from AssignmentProperties import gradeAssignments
from SimulationExecuter import simulationExecuter
from UI import make_Home, make_DirSetup, make_SimRunner, make_Grader
from SavingLoading import saveGrades, saveDirs, loadGrades, loadDirs

# -------------------------------
# Required Folder Setup Functions
# -------------------------------

test_names = ["test1a", "test1b", "test2", "test3a", "test3b"]

def StudentAssignmentFolder(general_path):
    dir_assignments = os.path.join(general_path, "all_assignments")
    if not os.path.exists(dir_assignments):
        os.makedirs(dir_assignments)
    print("all_assignments folder has been added")
    return dir_assignments

def MlModelFolder(test_names, general_path):
    dir_models = os.path.join(general_path, "ml_models")
    if not os.path.exists(dir_models):
        os.makedirs(dir_models)
    for test in test_names:
        test_model_dir = os.path.join(dir_models, test)
        if not os.path.exists(test_model_dir):
            os.makedirs(test_model_dir)
    print("ml_models folder has been added")
    return dir_models

# making a folder to store the scratch video files into
def ScratchFolder():
    dir_scratch = os.path.join(general_path, "scratch_videos")
    if not os.path.exists(dir_scratch):
        os.makedirs(dir_scratch)
    return dir_scratch

# run this function to get all group numbers of the uploaded assignments
def getAssignments():
    assignments = os.listdir(os.path.join(general_path, "all_assignments"))
    return assignments

# function to add sub-directories to store the video files of the tested simulations into
def FolderAdder(test_names):
    dir_simulations = os.path.join(general_path, "all_assignment_simulations")
    if not os.path.exists(dir_simulations):
        os.makedirs(dir_simulations)
    for test in test_names:
        test_dir = os.path.join(dir_simulations, test)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
    return dir_simulations


# ------------------------
# Defining all GUI windows
# ------------------------

window1, window2, window3, window4 = make_Home(), None, None, None

# -------------------------------------------------
# Making dispatch dictionary to store all functions
# -------------------------------------------------

dispatch_dictionary = {'Start Grading': gradeAssignments,
                       '-dir initializer-': StudentAssignmentFolder,
                       '-dir initializer2': MlModelFolder,
                       '-SIM EXECUTER-': simulationExecuter}

# ----------------------
# Initializing variables
# ----------------------

general_path = None
path_TwinCat = None
path_unity = None

sub_scores = None
final_scores = None

groups = []
sub_score_str_list = None

dir_assignments = None
dir_simulations = None
dir_models = None
dir_scratch = None

assignments = None

# ----------------------------------
# Loop to run GUI windows and events
# ----------------------------------

while True:
    window, event, values = sg.read_all_windows()

    if window == window1:
        if event == '-DIR SETUP-':
            window1.hide()
            if os.path.exists('savedData.json'):
                data = loadDirs()
                if general_path is None:
                    general_path = data[0]
                if path_TwinCat is None:
                    path_TwinCat = data[1]
                if path_unity is None:
                    path_unity = data[2]

            if os.path.exists('savedGrades.json'):
                scores = loadGrades()
                if sub_scores is None:
                    sub_scores = scores[0]
                if final_scores is None:
                    final_scores = scores[1]
                if len(groups) == 0 and len(scores) == 3:
                    groups = scores[2]

            window2 = make_DirSetup()
        elif event == '-SIM RUNNER-':
            window1.hide()
            if os.path.exists('savedData.json'):
                data = loadDirs()
                if general_path is None:
                    general_path = data[0]
                if path_TwinCat is None:
                    path_TwinCat = data[1]
                if path_unity is None:
                    path_unity = data[2]

            if os.path.exists('savedGrades.json'):
                scores = loadGrades()
                if sub_scores is None:
                    sub_scores = scores[0]
                if final_scores is None:
                    final_scores = scores[1]
                if len(groups) == 0 and len(scores) == 3:
                    groups = scores[2]

            window3 = make_SimRunner()
        elif event == '-GRADER-':
            window1.hide()
            if os.path.exists('savedData.json'):
                data = loadDirs()
                if general_path is None:
                    general_path = data[0]
                if path_TwinCat is None:
                    path_TwinCat = data[1]
                if path_unity is None:
                    path_unity = data[2]

            if os.path.exists('savedGrades.json'):
                scores = loadGrades()
                if sub_scores is None:
                    sub_scores = scores[0]
                if final_scores is None:
                    final_scores = scores[1]
                if len(groups) == 0 and len(scores) == 3:
                    groups = scores[2]

            window4 = make_Grader()
        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            break

    if window == window2:

        if event == '-SIM RUNNER-':
            window2.hide()
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            window3 = make_SimRunner()
        elif event == '-HOME-':
            window2.hide()
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            window1 = make_Home()
        elif event == "Submit directory" and len(values["-IN1-"]) != 0:
            general_path = values["-IN1-"]
            print("Added {} successfully".format(general_path))
        elif event == "Submit TwinCat" and len(values["-IN2-"]) != 0:
            path_TwinCat = values["-IN2-"]
            print("Added {} successfully".format(path_TwinCat))
        elif event == "Submit Unity" and len(values["-IN3-"]) != 0:
            path_unity = values["-IN3-"]
            print("Added {} successfully".format(path_unity))
        elif event == "-DIR INITIALIZER-":
            func_to_call = dispatch_dictionary['-dir initializer-']
            dir_assignments = func_to_call(values["-IN1-"])
        elif event == "-DIR INITIALIZER2-":
            func_to_call = dispatch_dictionary['-dir initializer2']
            dir_models = func_to_call(test_names, values["-IN1-"])
        elif event == sg.WIN_CLOSED:
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            break
        elif event == 'refresh':
            if general_path is not None:
                window.Element('input dir').Update(value=general_path)
            if path_TwinCat is not None:
                window.Element('input TwinCat').Update(value=path_TwinCat)
            if path_unity is not None:
                window.Element('input unity').Update(value=path_unity)

    if window == window3:
        if event == '-GRADER-':
            window3.hide()
            window4 = make_Grader()
        elif event == '-SIM EXECUTER-':
            window3.hide()
            FolderAdder(test_names)
            dir_scratch = FolderAdder(test_names)
            assignments = getAssignments()
            dir_simulations = FolderAdder(test_names)
            func_to_call = dispatch_dictionary['-SIM EXECUTER-']
            func_to_call(dir_simulations, dir_assignments,
                         assignments, path_unity,
                         path_TwinCat, test_names,
                         dir_scratch)
            time.sleep(5)
            window3.un_hide()
        elif event == '-HOME-':
            window3.hide()
            window1 = make_Home()
        elif event == sg.WIN_CLOSED:
            break

    if window == window4:
        if event == '-HOME-':
            window4.hide()
            window1 = make_Home()
            saveGrades(sub_scores, final_scores, groups)

        elif event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            sub_scores, final_scores = func_to_call(test_names, general_path)

            str_final = ""
            for final_score in final_scores:
                if len(str_final) == 0:
                    str_final = final_score
                else:
                    str_final = str_final + os.linesep + final_score
            window["grades"].update(value=str_final)
            saveGrades(sub_scores, final_scores, groups)

            nmbr_assignments = int(len(sub_scores) / 5)
            sub_score_str_list = np.zeros(shape=(nmbr_assignments, 5), dtype='object')
            count = 0
            for i in range(nmbr_assignments):
                for j in range(5):
                    sub_score_str_list[i][j] = sub_scores[j + count]

                count += 5

            groups = []
            for i in range(len(sub_score_str_list)):
                str = sub_score_str_list[i][0][6:9]
                groups.append(str)
            window["drop-down"].update(value=groups)

        elif event == 'refresh_grades':
            if sub_scores is not None:
                nmbr_assignments = int(len(sub_scores) / 5)
                sub_score_str_list = np.zeros(shape=(nmbr_assignments, 5),dtype='object')
                count = 0
                for i in range(nmbr_assignments):
                    for j in range(5):
                        sub_score_str_list[i][j] = sub_scores[j + count]

                    count += 5

                groups = []
                for i in range(len(sub_score_str_list)):
                    str = sub_score_str_list[i][0][6:9]
                    groups.append(str)
                window["drop-down"].update(value=groups)

            if final_scores is not None:
                str_final = ""
                for final_score in final_scores:
                    if len(str_final) == 0:
                        str_final = final_score
                    else:
                        str_final = str_final + os.linesep + final_score
                window["grades"].update(value=str_final)

        elif event == "select group":
            index = groups.index(values["drop-down"])
            st = ""
            for str in sub_score_str_list[index]:
                if len(st) == 0:
                    st = str
                else:
                    st = st + os.linesep + str
            window["selected group"].update(value=st)

        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            saveGrades(sub_scores, final_scores, groups)
            break

window.close()

