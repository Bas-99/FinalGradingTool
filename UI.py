'''
    *************************************************************
    *                          UI.py                            *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import PySimpleGUI as sg
from os import path

# --------------------------------------
# Importing functions from other modules
# --------------------------------------

from SavingLoading import loadGrades

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

groups = []

if path.exists("savedGrades.json"):
    data = loadGrades()
    groups = data[2]

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
        [sg.Combo(groups, key='drop-down'), sg.Button("select group")],
        [sg.Text("", key="grades", size=(50, 25), enable_events=True), sg.VSeparator(),
         sg.Text("", key='selected group', size=(50, 25))],
        [sg.Text("", size=(50, 1)), sg.VSeparator(), sg.Text("", size=(35, 1), key="nan evaluator"), sg.Button("yes - correct")],
        [sg.HSeparator()],
        [sg.Text("Export grades to directory"), sg.Button("Export Grades")],
        [sg.HSeparator()],
        [sg.Button('-HOME-'), sg.Button('-EXIT-')]
    ]
    return sg.Window('Grading Assignments', layout, finalize=True)
