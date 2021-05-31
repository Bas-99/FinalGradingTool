'''
    *************************************************************
    *                      makeTable.py                         *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import pandas as pd
import os
import openpyxl

# --------------------------
# Importing relevant modules
# --------------------------

from SavingLoading import loadGrades

# --------------------------------------------
# Function to retrieve scores from the strings
# --------------------------------------------

def get_score_from_str(string):

    # reading the values where the score is listed to see if nan
    if string[14:17] == 'nan':
        score = pd.NA
    # reading the value where the score is listed
    else:
        score = string[14]
        score = int(score)

    # returning the score
    return score

# ------------------------------------------
# Function to make a dataframe of the scores
# ------------------------------------------

def make_data_frame(general_path):

    # loading the saved grades and initializing variables
    data = loadGrades()
    test1 = []
    test2 = []
    test3 = []
    test4 = []
    test5 = []

    # looping over all grades in the savedGrades.json file
    for i in range(len(data[2])):

        # for each test, call the get_score_frome_str function
        # and feed in the string of the current group
        # this is done exactly the same for every test
        score1 = get_score_from_str(data[0][i * 5])
        test1.append(score1)

        score2 = get_score_from_str(data[0][i * 5 + 1])
        test2.append(score2)

        score3 = get_score_from_str(data[0][i * 5 + 2])
        test3.append(score3)

        score4 = get_score_from_str(data[0][i * 5 + 3])
        test4.append(score4)

        score5 = get_score_from_str(data[0][i * 5 + 4])
        test5.append(score5)

    # adding the computed data to their respective columns
    columns = {
        'Group': data[2],
        'Test 1': test1,
        'Test 2': test2,
        'Test 3': test3,
        'Test 4': test4,
        'Test 5': test5,
              }

    # writing the columns to a pandas dataframe
    df = pd.DataFrame(columns)

    # adding a row with the total scores per test
    df.loc['Total score per test', :] = df.sum(axis=0)

    # adding a column with the total scores per group
    df.loc[:, 'Total score (per group)'] = df.sum(axis=1)

    # writing the dataframe to an excel file
    df.to_excel(os.path.join(general_path, 'assignment_grades.xlsx'))
