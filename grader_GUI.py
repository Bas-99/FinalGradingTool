import PySimpleGUI as sg
import os.path
import os
from AssignmentProperties import gradeAssignments
import time
from SimulationExecuter import simulationExecuter

# -------------------------------
# Required Folder Setup Functions
# -------------------------------

test_names = ["test1a", "test1b", "test2", "test3a","test3b"]

def StudentAssignmentFolder(general_path):
    dir_assignments = os.path.join(general_path,"all_assignments")
    if not os.path.exists(dir_assignments):
        os.makedirs(dir_assignments)
    print("all_assignments folder has been added")
    return dir_assignments

def MlModelFolder(test_names,general_path):
    dir_models = os.path.join(general_path,"ml_models")
    if not os.path.exists(dir_models):
        os.makedirs(dir_models)
    for test in test_names:
        test_model_dir = os.path.join(dir_models,test)
        if not os.path.exists(test_model_dir):
            os.makedirs(test_model_dir)
    print("ml_models folder has been added")
    return dir_models

# making a folder to store the scratch video files into
def ScratchFolder():
    dir_scratch = os.path.join(general_path,"scratch_videos")
    if not os.path.exists(dir_scratch):
        os.makedirs(dir_scratch)
    return dir_scratch

# run this function to get all group numbers of the uploaded assignments
def getAssignments():
    assignments = os.listdir(os.path.join(general_path,"all_assignments"))
    return assignments

# function to add sub-directories to store the video files of the tested simulations into
def FolderAdder(test_names):
    dir_simulations = os.path.join(general_path,"all_assignment_simulations")
    if not os.path.exists(dir_simulations):
        os.makedirs(dir_simulations)
    for test in test_names:
        test_dir = os.path.join(dir_simulations,test)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
    return dir_simulations

# -------------------
# Defining GUI Layout
# -------------------

# defining the home screen of the GUI application for the autograding tool.
# this homescreen should contain a short introduction and navigation to
# all different use cases of the tool.
def make_Home():
    str_title = 'Welcome to the FESTO automated grading tool!'
    str_welcome = 'This tool is an aid in helping to grade 4TC00 assignments. \n' \
                  'Below you can select what functionalities you want to use. \n' \
                  'If this is the first time running the program, go to the directory setup. \n' \
                  'Otherwise you can go and run the simulations or if this is already done go to the grading.'
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
        [sg.Text(str_title, font=("Helvetica",25))],
        [sg.Image('Resources/festo.png',size=(1100,250))],
        [sg.HSeparator()],
        [sg.Text(str_welcome, font=("Helvetica",12)), ],
        [sg.HSeparator()],
        [sg.Text('Directory setup:',size=(20,1)),sg.VSeparator(),
         sg.Text('Simulation runner:',size=(20,1)),sg.VSeparator(),
         sg.Text('Grading assignments:',size=(20,1))],
        [sg.Button('-DIR SETUP-',size=(20,1),pad=(3,0)),sg.VSeparator(),
         sg.Button('-SIM RUNNER-',size=(20,1),pad=(3,0)),sg.VSeparator(),
         sg.Button('-GRADER-',size=(20,1),pad=(3,0))],
        [sg.HSeparator()],
        [sg.Button('-EXIT-')]
    ]
    return sg.Window('Home', layout, finalize=True)

# defining the directory setup window, this window should add the functionallity of selecting
# directories for general_path, Unity and TwinCat, furthermore it should contain the functionality
# to add the assignments to the general path.
def make_DirSetup():
    layout = [
        [sg.Text('Directory setup',font=("Helvetica", 15))],
        [sg.HSeparator()],
        [sg.Text('On this page, the general derectory, the TwinCat directory and Unity direcory have to be set.')],

        [sg.Text('Select a general directory:',size=(35,1)),
         sg.Input(size=(55,1)), sg.FolderBrowse(key="-IN1-"),sg.Button("Submit directory",size=(14,1))],

        [sg.Text('Select the directory for TwinCat (devenv.exe):',size=(35,1)),
         sg.Input(size=(55,1)), sg.FileBrowse(key="-IN2-"),sg.Button("Submit TwinCat",size=(14,1))],

        [sg.Text('Select the directory for Unity:',size=(35,1)),
         sg.Input(size=(55,1)),sg.FileBrowse(key="-IN3-"),sg.Button("Submit Unity",size=(14,1))],

        [sg.HSeparator()],
        [sg.Text('When the above three directories are specified, '
                 'the directory initializers can be run by clicking th buttons below:')],
        [sg.Button("-DIR INITIALIZER-"),sg.Button("-DIR INITIALIZER2-")],
        [sg.HSeparator()],
        [sg.Text("Please open the File Explorer and navigate to the specified general directory, \n"
                 "you will see the new all_assignments folder in which you have to un-zip the \n"
                 "to be graded files. When this is done, go to the next step")],
        [sg.HSeparator()],
        [sg.Button('-SIM RUNNER-'),sg.Button('-HOME-')]
    ]
    return sg.Window('Directory setup', layout, finalize=True)

def make_SimRunner():
    layout = [
        [sg.Text('Simulation runner',font=("Helvetica", 15))],
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
    return sg.Window('Simulation runner',layout,finalize=True)

def make_Grader():
    layout = [
        [sg.Text('Grading Assignments',font=("Helvetica", 15))],
        [sg.HSeparator()],
        [sg.Text('On this page the recorded tests performed on the assignments can be graded')],
        [sg.Text('Click here to start grading:'),sg.Button('Start Grading')],
        [sg.HSeparator()],
        [sg.Text("Results for tested assignments",font=("Helvetica", 13))],
        [sg.Text("",key="grades",size=(50,25))],
        [sg.HSeparator()],
        [sg.Text("Export grades to directory"), sg.Button("Export Grades")],
        [sg.HSeparator()],
        [sg.Button('-HOME-'), sg.Button('-EXIT-')]
    ]
    return sg.Window('Grading Assignments', layout, finalize=True)

window1, window2, window3, window4 = make_Home(), None, None, None

dir_list = []

dispatch_dictionary = {'Start Grading':gradeAssignments,
                       '-dir initializer-':StudentAssignmentFolder,
                       '-dir initializer2':MlModelFolder,
                       '-SIM EXECUTER-':simulationExecuter}

general_path = None
path_TwinCat = None
path_unity = None
dir_assignments = None
dir_simulations = None
assignments = None
dir_scratch = None

# ----------------------
# Running Functional GUI
# ----------------------

while True:
    window, event, values = sg.read_all_windows()

    if window == window1:
        if event == '-DIR SETUP-':
            window1.hide()
            window2 = make_DirSetup()
        elif event == '-SIM RUNNER-':
            window1.hide()
            window3 = make_SimRunner()
        elif event == '-GRADER-':
            window1.hide()
            window4 = make_Grader()
        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            break

    if window == window2:
        if event == '-SIM RUNNER-':
            window2.hide()
            window3 = make_SimRunner()
        elif event == '-HOME-':
            window2.hide()
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
            break

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
        elif event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            sub_scores, final_scores = func_to_call(os.path.join(general_path, "all_assignment_simulations"),
                                                    os.path.join(general_path, "ml_models"),
                                                    test_names)
            str = ""
            for final_score in final_scores:
                if len(str) == 0:
                    str = final_score
                else:
                    str = str + os.linesep + final_score
            window["grades"].update(value=str)
            print(str)
        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            break

window.close()

