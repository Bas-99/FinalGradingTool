import time
import os
from tensorflow.keras.models import load_model
from Video2Frames import create_data
import numpy as np

# -------------------------------
# Defining A Class for Assignment
# -------------------------------

class Assignment(object):
    _counter = 0

    def __init__(self, group, scores=None):
        if scores is None:
            scores = []
        Assignment._counter += 1
        self.group = group
        self.scores = scores

    def setScore(self, score):
        self.scores.append(score)

    def getFinalScore(self):
        return sum(self.scores)

    def getSubScoreString(self, assignment, cnt, test_name):
        str = "Group {} got {} points for {}".format(
            assignment.group, assignment.scores[cnt], test_name
        )
        return str

    def getFinalScoreString(self, assignment,test_names):
        str = "Group {} got {} points out of {} total".format(
            assignment.group, assignment.getFinalScore(), len(test_names)
        )
        return str

# -----------------------------------------
# Function to Instances to Class Assignment
# -----------------------------------------

def gradeAssignments(dir,dirm,test_names):
    seq_len = [250, 350, 350, 350, 350]
    dir_simulations = dir
    dir_models = dirm
    classes = ["correct", "incorrect"]

    assignments = []
    count = 0

    for name in test_names:
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

            classif = np.argmax(prediction, axis=1)

            # reading the group number from the file names
            files = []
            for file in os.listdir(test_path):
                if file.endswith(".avi"):
                    files.append(file)

            # rewarding score if the test has been completed correctly
            if classes[classif[0]] == "correct":
                score += 1

            if count == 0:
                new_assignment = Assignment(files[name_counter][-7:-4])
                new_assignment.setScore(score)

                assignments.append(new_assignment)
            else:
                assignments[name_counter].setScore(score)

            name_counter += 1

        count += 1
        end_test = time.time()
        duration = end_test - start_test
        print("Grading {} took {} seconds".format(name, duration))

    sub_scores = []
    final_scores = []

    for assignment in assignments:
        cnt = 0
        for test_name in test_names:
            sub_score = assignment.getSubScoreString(assignment, cnt, test_name)
            sub_scores.append(sub_score)
            cnt += 1
        final_score = assignment.getFinalScoreString(assignment,test_names)
        final_scores.append(final_score)

    return sub_scores, final_scores
