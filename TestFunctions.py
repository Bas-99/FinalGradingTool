'''
    *************************************************************
    *                      TestFunctions.py                     *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import time
import functools

# --------------------------------------
# Importing functions from other Modules
# --------------------------------------

from buttons import add1, add2, add3, fill1, startButton, autoSwitchOn

# ---------------------------------
# Definition of function for test 1
# ---------------------------------

time_test1a = 25

def firstTestA():
    add1()  # add 1 block in first stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add3()  # add 1 block in third stack
    time.sleep(1)
    startButton()  # press the start button
    print("First test part 1 is started")

# ---------------------------------
# Definition of function for test 2
# ---------------------------------

time_test1b = 35

def firstTestB():
    add1()  # add 1 block in first stack
    time.sleep(1)
    add1()  # add 1 block in first stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add3()  # add 1 block in third stack
    time.sleep(1)
    add3()  # add 1 block in third stack
    time.sleep(1)
    autoSwitchOn()  # turn the auto switch to auto-mode
    time.sleep(1)
    startButton()  # press the start button
    print("First test part 2 is started")

# ---------------------------------
# Definition of function for test 3
# ---------------------------------

time_test2 = 35

def secondTest():
    add1()  # add 1 block in first stack
    time.sleep(1)
    add1()  # add 1 block in first stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add3()  # add 1 block in third stack
    time.sleep(1)
    add3()  # add 1 block in third stack
    time.sleep(1)
    autoSwitchOn()  # turn the auto switch to auto-mode
    time.sleep(1)
    startButton()  # press the start button
    print("Second test is started")

# ---------------------------------
# Definition of function for test 4
# ---------------------------------

time_test3a = 35

def thirdTestA():
    fill1()  # fill the first stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    add2()  # add 1 block in second stack
    time.sleep(1)
    autoSwitchOn()  # turn the auto switch to auto-mode
    time.sleep(1)
    startButton()  # press the start button
    print("Third test part 1 is started")

# ---------------------------------
# Definition of function for test 5
# ---------------------------------

time_test3b = 35

def thirdTestB():
    fill1()  # fill the first stack
    time.sleep(1)
    add3()  # add 1 block in second stack
    time.sleep(1)
    add3()  # add 1 block in second stack
    time.sleep(1)
    autoSwitchOn()  # turn the auto switch to auto-mode
    time.sleep(1)
    startButton()  # press the start button
    print("Third test part 2 is started")

# --------------------------------------
# Adding all functions to function array
# --------------------------------------

test_list = []
test_list.append(functools.partial(firstTestA))
test_list.append(functools.partial(firstTestB))
test_list.append(functools.partial(secondTest))
test_list.append(functools.partial(thirdTestA))
test_list.append(functools.partial(thirdTestB))
