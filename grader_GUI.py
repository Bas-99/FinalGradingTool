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
import json
import time

# --------------------------------------
# Importing functions from other modules
# --------------------------------------

from AssignmentProperties import gradeAssignments
from SimulationExecuter import simulationExecuter

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

# ---------------------------
# Defining GUI Window Layouts
# ---------------------------

# defining the home screen of the GUI application for the autograding tool.
# this homescreen should contain a short introduction and navigation to
# all different use cases of the tool.
def make_Home():
    str_title = 'Welcome to the FESTO automated grading tool!'
    str_welcome = 'This tool is an aid in helping to grade 4TC00 assignments. \n' \
                  'Below you can select what functionalities you want to use. \n' \
                  'If this is the first time running the program, go to the ' \
                  'directory setup. \n' \
                  'Otherwise you can go and run the simulations ' \
                  'or if this is already done go to the grading.'
    column1 = (
        [sg.Text('Directory setup:')],
        [sg.Button('-DIR SETUP-')]
    )
    column2 = (
        [sg.Text('Simulation runner:')],
        [sg.Button('-SIM RUNNER-')]
    )

    column3 = (
        [sg.Text('Grading assignments:')],
        [sg.Button('-GRADER-')]
    )

    layout = [
        [sg.Text(str_title, font=("Helvetica", 25))],
        [sg.Image('Resources/festo.png', size=(1100, 250))],
        [sg.HSeparator()],
        [sg.Text(str_welcome, font=("Helvetica",12)), ],
        [sg.HSeparator()],

        [sg.Text('Directory setup:', size=(20, 1)), sg.VSeparator(),
         sg.Text('Simulation runner:', size=(20, 1)), sg.VSeparator(),
         sg.Text('Grading assignments:', size=(20, 1))],

        [sg.Button('-DIR SETUP-', size=(20, 1), pad=(3, 0)), sg.VSeparator(),
         sg.Button('-SIM RUNNER-', size=(20, 1), pad=(3, 0)), sg.VSeparator(),
         sg.Button('-GRADER-', size=(20, 1), pad=(3, 0))],

        [sg.HSeparator()],
        [sg.Button('-EXIT-')]
    ]
    return sg.Window('Home', layout, finalize=True)

# defining the directory setup window, this window should add the functionallity of selecting
# directories for general_path, Unity and TwinCat, furthermore it should contain the functionality
# to add the assignments to the general path.
def make_DirSetup():
    layout = [
        [sg.Text('Directory setup',font=("Helvetica", 15)), sg.Button('refresh')],
        [sg.HSeparator()],
        [sg.Text('On this page, the general directory, '
                 'the TwinCat directory and Unity directory have to be set.')],

        [sg.Text('Select a general directory:', size=(35, 1)),
         sg.Input(size=(55, 1), key='input dir'), sg.FolderBrowse(key="-IN1-"),
         sg.Button("Submit directory", size=(14, 1))],

        [sg.Text('Select the directory for TwinCat (devenv.exe):', size=(35, 1)),
         sg.Input(size=(55, 1), key='input TwinCat'), sg.FileBrowse(key="-IN2-"),
         sg.Button("Submit TwinCat", size=(14, 1))],

        [sg.Text('Select the directory for Unity:', size=(35, 1)),
         sg.Input(size=(55, 1), key='input unity'), sg.FileBrowse(key="-IN3-"),
         sg.Button("Submit Unity", size=(14, 1))],

        [sg.HSeparator()],
        [sg.Text('When the above three directories are specified, '
                 'the directory initializers can be run by clicking th buttons below:')],
        [sg.Button("-DIR INITIALIZER-"), sg.Button("-DIR INITIALIZER2-")],
        [sg.HSeparator()],
        [sg.Text("Please open the File Explorer and navigate to the specified general directory, \n"
                 "you will see the new all_assignments folder in which you have to un-zip the \n"
                 "to be graded files. When this is done, go to the next step")],
        [sg.HSeparator()],
        [sg.Button('-SIM RUNNER-'), sg.Button('-HOME-')]
    ]
    return sg.Window('Directory setup', layout, finalize=True)

def make_SimRunner():
    layout = [
        [sg.Text('Simulation runner', font=("Helvetica", 15))],
        [sg.HSeparator()],
        [sg.Text("Click the button below to start executing the tests on the uploaded assignments. \n"
                 "Take care of the following points: \n"
                 "  -   You are NOT able to use your PC, while the program is running tests \n"
                 "  -   You should make sure there is no other program running. \n"
                 "  -   You should make sure no other window is opened. \n"
                 "  -   You should run this program on one single 1080p monitor.")],
        [sg.Button('-SIM EXECUTER-')],
        [sg.HSeparator()],
        [sg.Button('-GRADER-'), sg.Button('-HOME-')]
    ]
    return sg.Window('Simulation runner', layout, finalize=True)

all_results = []

def make_Grader():
    layout = [
        [sg.Text('Grading Assignments', font=("Helvetica", 15)),sg.Button("refresh_grades")],
        [sg.HSeparator()],
        [sg.Text('On this page the recorded tests performed on the assignments can be graded')],
        [sg.Text('Click here to start grading:'), sg.Button('Start Grading')],
        [sg.HSeparator()],
        [sg.Text("Final scores per assignments", font=("Helvetica", 13), size=(35, 1)), sg.VSeparator(),
         sg.Text("Sub-scores for selected assignment", font=("Helvetica", 13), size=(35, 1))],
        [sg.HSeparator()],
        [sg.Combo(groups, key='drop-down'),sg.Button("select group")],
        [sg.Text("", key="grades", size=(50, 25), enable_events=True), sg.VSeparator(),
         sg.Text("", key='selected group', size=(50, 25))],
        [sg.HSeparator()],
        [sg.Text("Export grades to directory"), sg.Button("Export Grades")],
        [sg.HSeparator()],
        [sg.Button('-HOME-'), sg.Button('-EXIT-')]
    ]
    return sg.Window('Grading Assignments', layout, finalize=True)

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

