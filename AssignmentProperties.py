'''
    *************************************************************
    *                  AssignmentProperties.py                  *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import time
import os
import numpy as np
from tensorflow.keras.models import load_model

# --------------------------------------
# Importing functions from other Modules
# --------------------------------------

from Video2Frames import create_data

# -------------------------------
# Defining A Class for Assignment
# -------------------------------

class Assignment(object):
    _counter = 0
    instances = []

    # initializing the Assignment class
    def __init__(self, group, scores=None):
        if scores is None:
            scores = []
        Assignment._counter += 1
        self.instances.append(self)
        self.group = group
        self.scores = scores

    # setting the sub scores for a Assignment instance
    def setScore(self, score):
        self.scores.append(score)

    # retrieving the final score from the sub scores of an instance
    def getFinalScore(self):
        return sum(self.scores)

    # retrieving the string including the sub scores
    def getSubScoreString(self, assignment, cnt, test_name):
        str_score = "Group {} got {} points for {}".format(
            assignment.group, assignment.scores[cnt], test_name
        )
        return str_score

    # retrieving the string including the final scores
    def getFinalScoreString(self, assignment, test_names):
        str_final = "Group {} got {} points out of {} total".format(
            assignment.group, assignment.getFinalScore(), len(test_names)
        )
        return str_final

# -----------------------------------------
# Function to Instances to Class Assignment
# -----------------------------------------

def gradeAssignments(test_names, general_path):
    # setting some variables, which are used in the grading process
    seq_len = [250, 350, 350, 350, 350]
    dir_simulations = os.path.join(general_path, "all_assignment_simulations")
    dir_models = os.path.join(general_path, "ml_models")
    classes = ["correct", "incorrect"]

    assignments = []
    exceptional_cases = []
    count = 0

    # looping over every test in test_names
    for name in test_names:

        # starting a timer and joining the directories to the
        # corresponding test in the loop
        start_test = time.time()
        test_path = os.path.join(dir_simulations, name)
        file_path = os.path.join(dir_models, name)

        # loading the ML model
        new_model = load_model(file_path, compile=True)

        # storing the data to X
        X = create_data(test_path, seq_len[test_names.index(name)])

        name_counter = 0

        # looping over all different videos in the data array X
        for x in X:
            score = 0
            sample_to_predict = np.array([x])

            # making a prediction using the ML model
            prediction = new_model.predict(sample_to_predict)

            # reading the group number from the file names
            files = []
            for file in os.listdir(test_path):
                if file.endswith(".avi"):
                    files.append(file)

            # uncomment section below to print the accuracy and the group number (used for testing)
            # print(prediction[0][0])
            # print(files[name_counter][-7:-4])

            # adding an accuracy range to filter out the exceptional cases
            acc_range = 0.75
            # below the exceptional cases will be filtered
            if 1 - acc_range < prediction[0][0] < acc_range:
                exceptional_cases.append(count)

                if count == 0:
                    new_assignment = Assignment(files[name_counter][-7:-4])
                    new_assignment.setScore(np.NaN)

                    assignments.append(new_assignment)
                else:
                    assignments[name_counter].setScore(np.NaN)

            # below the scores for non exceptional cases are computed
            else:
                classif = np.argmax(prediction, axis=1)

                # rewarding score if the test has been completed correctly
                if classes[classif[0]] == "correct":
                    score += 1

                # setting the scores to a Assignment class instance
                if count == 0:
                    new_assignment = Assignment(files[name_counter][-7:-4])
                    new_assignment.setScore(score)

                    assignments.append(new_assignment)
                else:
                    assignments[name_counter].setScore(score)

            name_counter += 1

        # computing the grading duration and printing it in the Python console
        count += 1
        end_test = time.time()
        duration = end_test - start_test
        print("Grading {} took {} seconds".format(name, duration))

    # initializing two lists for the scores
    sub_scores = []
    final_scores = []

    # looping over all Assignment class instances
    for assignment in assignments:
        cnt = 0

        # looping over all tests for each class instance
        for test_name in test_names:

            # computing the sub score strings for each test
            sub_score = assignment.getSubScoreString(assignment, cnt, test_name)
            sub_scores.append(sub_score)
            cnt += 1

        # computing the final score strings for each group
        final_score = assignment.getFinalScoreString(assignment, test_names)
        final_scores.append(final_score)

    # adding all scores to one variable
    all_scores = sub_scores + final_scores

    # saving/writing the all_scores variable to final_grades.txt file
    grade_file_name = "final_grades.txt"
    completeName = os.path.join(general_path, grade_file_name)

    grade_file = open(completeName, "w")
    for line in all_scores:
        grade_file.write('{}\n'.format(line))
    grade_file.close()

    # returning the sub_scores and final_scores variables
    return sub_scores, final_scores

