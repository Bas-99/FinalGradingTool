#----------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------buttons.py--------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
# This file defines all physical buttons existing in the Digital Twin environment. Every button has its own function   #
# such that one can call a different sequence of buttons, which will result in a different setup or action.            #
#----------------------------------------------------------------------------------------------------------------------#

import pyautogui
import time

# defining the buttons for the digital twin environment.

def fill1():
    # filling the left stack
    pyautogui.click(360, 507)

def fill2():
    # filling the middle stack
    pyautogui.click(400, 507)

def fill3():
    # filling the right stack
    pyautogui.click(440, 507)

def add1():
    # filling the left stack
    pyautogui.click(361, 476)

def add2():
    # filling the middle stack
    pyautogui.click(399, 477)

def add3():
    # filling the right stack
    pyautogui.click(440, 477)

def autoSwitchOn():
    # switching to automatic mode
    pyautogui.mouseDown(318, 488)
    time.sleep(2)
    pyautogui.mouseUp()

def autoSwitchOff():
    pyautogui.mouseDown(318, 488, button='right')
    time.sleep(2)
    pyautogui.mouseUp(button='right')

def startButton():
    # right-click the start button to start the simulation
    pyautogui.click(287, 462, button='right')

def resetButton():
    # pressing the reset button
    pyautogui.click(287,488)

def stopButton():
    # pressing the stop button
    pyautogui.click(319,464)

def testButton():
    print("test")