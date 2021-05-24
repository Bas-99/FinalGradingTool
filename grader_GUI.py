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

from AssignmentProperties import gradeAssignments, Assignment
from SimulationExecuter import simulationExecuter
from UI import make_Home, make_DirSetup, make_SimRunner, make_Grader
from SavingLoading import saveGrades, saveDirs, loadGrades, loadDirs

# -------------------------------
# Required Folder Setup Functions
# -------------------------------

# adding the test names for the different tests
test_names = ["test1a", "test1b", "test2", "test3a", "test3b"]

# adding a directory to store all student assignments into
def StudentAssignmentFolder(general_path):
    dir_assignments = os.path.join(general_path, "all_assignments")
    if not os.path.exists(dir_assignments):
        os.makedirs(dir_assignments)
    print("all_assignments folder has been added")
    return dir_assignments

# Adding a folders for the different (already trained machine learning models)
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
exceptional_cases = []

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

    # code for the first window (home screen), the program starts from this window
    # and will return this window if the corresponding event is initialized
    if window == window1:

        # action when the -DIR SETUP- button is pressed
        # hide the home window, load all relevant variables (if available),
        # finally show the dir setup window
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

        # action when the -SIM RUNNER- button is pressed
        # hide the home window, load relevant variables and
        # show the sim runner window
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

        # action if the -GRADER- button is pressed
        # hide the home window, load relevant variables,
        # show the make grader window
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

        # action if the -EXIT- button is pressed
        # the GUI will be closed
        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            break

    # code for the second window (the directory setup window), in this window
    # the paths/directories will be setup. This is done by asking for user input in the GUI
    if window == window2:

        # action if the -SIM RUNNER- button is pressed
        # hide the directory setup window, save the input paths,
        # show the simulation runner window
        if event == '-SIM RUNNER-':
            window2.hide()
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            window3 = make_SimRunner()

        # action if the -HOME- button is pressed
        # hide the directory setup window, save the input paths,
        # show the home window
        elif event == '-HOME-':
            window2.hide()
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            window1 = make_Home()

        # action if the Submit directory button is pressed
        # the general_path variable will be changed to the one specified by the user
        # printing of string in Python console if done correctly
        elif event == "Submit directory" and len(values["-IN1-"]) != 0:
            general_path = values["-IN1-"]
            print("Added {} successfully".format(general_path))

        # action if the Submit TwinCat button is pressed
        # the path_TwinCat variable will be changed to the one specified by the user
        # printing of string in Python console if done correctly
        elif event == "Submit TwinCat" and len(values["-IN2-"]) != 0:
            path_TwinCat = values["-IN2-"]
            print("Added {} successfully".format(path_TwinCat))

        # action if the Submint Unity button is pressed
        # the path_unity variable is changed to the one specified by the user
        # printing of string in Python console if done correctly
        elif event == "Submit Unity" and len(values["-IN3-"]) != 0:
            path_unity = values["-IN3-"]
            print("Added {} successfully".format(path_unity))

        # action if the -DIR INITIALIZER- button is pressed
        # calling the StudentAssignmentFolder function from the dispatch dictionary
        # setting the dir_assignments variable equal to the returned value of the function
        elif event == "-DIR INITIALIZER-":
            func_to_call = dispatch_dictionary['-dir initializer-']
            dir_assignments = func_to_call(values["-IN1-"])

        # action if the -DIR INITIALIZER2- button is pressed
        # calling the MlModelFolder function from the dispatch dictionary
        # setting the dir_models variable equal to the returned value of the function
        elif event == "-DIR INITIALIZER2-":
            func_to_call = dispatch_dictionary['-dir initializer2']
            dir_models = func_to_call(test_names, values["-IN1-"])

        # action if the window is closed
        # saving all the paths/directories and breaking out of the loop
        elif event == sg.WIN_CLOSED:
            saveDirs(general_path, path_TwinCat, path_unity, dir_assignments, dir_models)
            break

        # action if the refresh button is pressed
        # if the paths/directories already have been filled in before,
        # it will load the variables from savedData.json
        elif event == 'refresh':
            if general_path is not None:
                window.Element('input dir').Update(value=general_path)
            if path_TwinCat is not None:
                window.Element('input TwinCat').Update(value=path_TwinCat)
            if path_unity is not None:
                window.Element('input unity').Update(value=path_unity)

    # code for the third window (simulation runner window), in this window
    # the simulation executer will be initiated to run and record all simulations
    if window == window3:

        # action if the -GRADER- button is pressed
        # hide the current window and show the make grader window
        if event == '-GRADER-':
            window3.hide()
            window4 = make_Grader()

        # action if the -SIM EXECUTER- button is pressed
        # hiding the current window, adding the scratch folder, retrieving the
        # assignments from the getAssignments function, add the folder to store all
        # the recorded simulations into, call the simulationExecuter function from
        # the dispatch dictionary, when finished unhide the window again
        elif event == '-SIM EXECUTER-':
            window3.hide()
            dir_scratch = ScratchFolder()
            assignments = getAssignments()
            dir_simulations = FolderAdder(test_names)
            func_to_call = dispatch_dictionary['-SIM EXECUTER-']
            func_to_call(dir_simulations, dir_assignments,
                         assignments, path_unity,
                         path_TwinCat, test_names,
                         dir_scratch)
            time.sleep(5)
            window3.un_hide()

        # action if the -HOME- button is pressed
        # hide the current window and show the home window
        elif event == '-HOME-':
            window3.hide()
            window1 = make_Home()

        # action if the window is closed
        # break out of the loop and close the GUI
        elif event == sg.WIN_CLOSED:
            break

    # code for the fourth window (simulation grader window), in this window
    # the assignments will be graded and the grades will be shown in the GUI
    # furthermore can the teacher evaluate the tests, which are graded with
    # lower accuracy than the norm
    if window == window4:

        # action if the -HOME- button is pressed
        # close the current window and open the home window
        # save the scores and graded groups if they exist
        if event == '-HOME-':
            window4.hide()
            window1 = make_Home()
            saveGrades(sub_scores, final_scores, groups)

        # action if the Start Grading button is pressed
        # this will call the gradeAssignments function from the dispatch dictionary
        # the sub_scores and final_scores variables will be changed to the returned
        # values by the called function.
        elif event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            sub_scores, final_scores = func_to_call(test_names, general_path)

            # str_final is made, which contains strings, with all the final scores for every group,
            # which will be displayed inside the GUI, the computed grades will be
            # saved to savedGrades.json.
            str_final = ""
            for final_score in final_scores:
                if len(str_final) == 0:
                    str_final = final_score
                else:
                    str_final = str_final + os.linesep + final_score

            window["grades"].update(value=str_final)
            saveGrades(sub_scores, final_scores, groups)

            # Then a matrix, (sub_score_str_list) is made which is filled with all
            # sub_scores per group at last the graded group numbers are
            # added to the drop-down menu
            nmbr_assignments = int(len(sub_scores) / 5)
            sub_score_str_list = np.zeros(shape=(nmbr_assignments, 5), dtype='object')
            count = 0
            for i in range(nmbr_assignments):
                for j in range(5):
                    sub_score_str_list[i][j] = sub_scores[j + count]

                count += 5

            data2 = loadGrades()
            groups2 = data2[2]
            window["drop-down"].update(value=groups2)

        # action if the refresh_grades button is pressed
        elif event == 'refresh_grades':

            # if the sub_scores variable is not None, read the values
            # from the sub_score_str_list matrix and add their group
            # numbers to the drop-down menu
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

            # if the final_scores variable is not None, read the values
            # from final_scores and add them to a string, which is
            # contains all final scores (spaced out vertically)
            # show this string inside the GUI
            if final_scores is not None:
                str_final = ""
                for final_score in final_scores:
                    if len(str_final) == 0:
                        str_final = final_score
                    else:
                        str_final = str_final + os.linesep + final_score
                window["grades"].update(value=str_final)

        # action if the select group button is pressed
        # read the group number from the selected group in the drop-down menu
        elif event == "select group":
            index = groups.index(values["drop-down"])

            # make a string which contains all scores per test for the selected group
            # displaying the string inside the GUI
            st = ""
            for str in sub_score_str_list[index]:
                if len(st) == 0:
                    st = str
                else:
                    st = st + os.linesep + str
            window["selected group"].update(value=st)

            # for every nan inside the sub grades, raise the question if
            # this test is computed correct and incorrect (solving the exceptional cases)
            for line in range(len(sub_score_str_list[index])):
                if sub_score_str_list[index][line][14:17] == "nan":
                    question = "Is {} of group {} correct?".format(sub_score_str_list[index][line][29:35],
                                                                   sub_score_str_list[index][line][0:9])
                    exceptional_cases.append(question)

            # displaying the question for the exceptional cases for the selected group
            if len(exceptional_cases) == 0:
                pass
            else:
                window["nan evaluator"].update(value=exceptional_cases[0])

        # action if the correct button is pressed
        elif event == 'correct':

            if len(exceptional_cases) == 0:
                pass
            else:
                # read the index from the drop-down menu
                index = groups.index(values["drop-down"])

                # computing the group index (5 tests per group)
                group = index * 5
                test = 0

                # reading what test resulted in the exceptional case
                # this has to be done different for test2 as this string
                # is one shorter than the other tests
                if not exceptional_cases[0][3:9] == 'test2 ':
                    test = test_names.index(exceptional_cases[0][3:9])
                else:
                    test = test_names.index(exceptional_cases[0][3:8])

                # changing the nan in the sub_scores variable to a 1
                sub_scores[test + group] = sub_scores[test + group].replace('nan', '1')

                # computing the new final_score with the adjusted sub_scores
                new_final_scores = []
                for i in range(0, 5):
                    if sub_scores[group + i][14:17] == 'nan':
                        break
                    else:
                        new_score = int(sub_scores[group + i][14])
                        new_final_scores.append(new_score)

                new_final_score = sum(new_final_scores)

                # replace the final_score variable for a group if all
                # exceptional cases are checked
                if len(new_final_scores) == 5:
                    final_scores[index] = final_scores[index].replace('nan', "{}".format(new_final_score))

                # showing the updated final_scores inside the GUI
                if final_scores is not None:
                    str_final = ""
                    for final_score in final_scores:
                        if len(str_final) == 0:
                            str_final = final_score
                        else:
                            str_final = str_final + os.linesep + final_score
                    window["grades"].update(value=str_final)

                # going on to the next exceptional case if there is still one left
                exceptional_cases = exceptional_cases[1:]
                if len(exceptional_cases) == 0:
                    pass
                else:
                    window["nan evaluator"].update(value=exceptional_cases[0])

                # update the evaluated (changed) sub_scores inside the GUI
                sub_score_str_list[index][test] = sub_scores[test + group]

                st = ""
                for str in sub_score_str_list[index]:
                    if len(st) == 0:
                        st = str
                    else:
                        st = st + os.linesep + str
                window["selected group"].update(value=st)

                # saving the adjusted grades to the savedGrades.json file
                saveGrades(sub_scores, final_scores, groups)

        # action if the incorrect button is pressed
        elif event == 'incorrect':

            if len(exceptional_cases) == 0:
                pass
            else:
                # reading the index from the drop-down menu
                index = groups.index(values["drop-down"])

                # computing the group index (5 tests per group)
                group = index * 5
                test = 0

                # reading what test resulted in the exceptional case
                # this has to be done different for test2 as this string
                # is one shorter than the other tests
                if not exceptional_cases[0][3:9] == 'test2 ':
                    test = test_names.index(exceptional_cases[0][3:9])
                else:
                    test = test_names.index(exceptional_cases[0][3:8])

                # replacing the nan values for 0 in the sub_scores variable
                sub_scores[test + group] = sub_scores[test + group].replace('nan', '0')

                # computing the new final_score for the adjusted sub_scores
                new_final_scores = []
                for i in range(0, 5):
                    if sub_scores[group + i][14:17] == 'nan':
                        break
                    else:
                        new_score = int(sub_scores[group + i][14])
                        new_final_scores.append(new_score)

                new_final_score = sum(new_final_scores)

                # if all exceptional cases are solved, replace the final_scores
                # variable with the new final score
                if len(new_final_scores) == 5:
                    final_scores[index] = final_scores[index].replace('nan', "{}".format(new_final_score))

                # displaying the newly computed final scores inside the GUI
                if final_scores is not None:
                    str_final = ""
                    for final_score in final_scores:
                        if len(str_final) == 0:
                            str_final = final_score
                        else:
                            str_final = str_final + os.linesep + final_score
                    window["grades"].update(value=str_final)

                # going to the next exceptional case if there are still left
                exceptional_cases = exceptional_cases[1:]
                if len(exceptional_cases) == 0:
                    pass
                else:
                    window["nan evaluator"].update(value=exceptional_cases[0])

                # updating the sub_scores inside the GUI
                sub_score_str_list[index][test] = sub_scores[test + group]

                st = ""
                for str in sub_score_str_list[index]:
                    if len(st) == 0:
                        st = str
                    else:
                        st = st + os.linesep + str
                window["selected group"].update(value=st)

                # saving the new scores to the savedGrades.json file
                saveGrades(sub_scores, final_scores, groups)

        # action if the -EXIT- button is pressed
        # save the sub_scores and final_scores and graded groups
        # to savedGrades.json, break out of the loop
        elif event == '-EXIT-' or event == sg.WIN_CLOSED:
            saveGrades(sub_scores, final_scores, groups)
            break

# close the current window if broken out of the loop
window.close()

