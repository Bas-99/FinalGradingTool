'''
    *************************************************************
    *                   ProgramExecuter.py                      *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import os
import pyautogui
import ctypes
import psutil
import time
import os.path
import signal

# ------------------------------
# App Runner function definition
# ------------------------------

def appRunner(path_unity, path_TwinCat, folder_dh_DT):
    global run_once

    # definition of the required file names (standard names)
    dir_sim = path_unity

    dir_Twin = path_TwinCat

    sim_folder = 'TwinCAT template Digital Twin'
    sim_file = 'dh_plc_DT.sln'

    file_dh_DT = 'dh_DT.xml'
    dir_dh_DT = os.path.join(folder_dh_DT, file_dh_DT).replace("/", "\\")

    # the following line will open the TwinCat program
    if "devenv.exe" in (i.name() for i in psutil.process_iter()):
        print("TwinCat is already opened")
        # force it to close TwinCat?
    else:
        os.startfile(dir_Twin)
    time.sleep(2)

    # this part will make sure the window TwinCat window is maximized
    pyautogui.keyDown('alt')
    pyautogui.press(' ')
    pyautogui.press('x')
    pyautogui.keyUp('alt')
    time.sleep(2)

    # press the FILE button, top left (1920x1080), and open project/solution
    pyautogui.click(28, 50)
    pyautogui.moveTo(28, 109, duration=0.2, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(465, 109, duration=0.4, tween=pyautogui.easeInOutQuad)
    pyautogui.click(465, 109)
    time.sleep(2)

    # search for the simulation file in the already opened file explorer
    pyautogui.write(sim_folder)
    pyautogui.press('enter')
    pyautogui.write(sim_file)
    pyautogui.press('enter')

    # navigating through the menu on the left to go to the CIF folder
    time.sleep(15)
    pyautogui.click(102, 272)
    time.sleep(0.5)
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    time.sleep(0.5)

    # on the CIF folder import the XML file
    pyautogui.keyDown('shift')
    pyautogui.press('f10')
    pyautogui.keyUp('shift')
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)

    # now the right XML file is chosen and imported, all files will be replaced
    pyautogui.write(dir_dh_DT)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(3)

    # the runtime will be activated and restarted
    pyautogui.click(262, 113)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(10)
    pyautogui.press('enter')
    time.sleep(5)

    # the system will login on the corresponding port
    pyautogui.click(1004, 113)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)

    # the unity simulation is started
    if "Festo MPS Distributing and Handling.exe" in (i.name() for i in psutil.process_iter()):
        print("Unity is already opened")
        # force it to close unity?
    else:
        os.startfile(dir_sim)
    time.sleep(5)

    # the system switches back to TwinCat to login into the simulation
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    time.sleep(2)
    pyautogui.click(1029, 113)

    # the simulation window is reopened and maximized
    time.sleep(5)
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMISE = 3
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMISE)
    time.sleep(5)

# ------------------------------
# App Closer function definition
# ------------------------------

def appCloser():

    # checking if TwinCat is active, if this is true than close the application
    for pid in (process.pid for process in psutil.process_iter() if process.name() == "devenv.exe"):
        os.kill(pid,signal.SIGTERM)
    print("TwinCat successfully closed")

    # checking if Unity is active, if this is true than close the application
    for pid in (process.pid for process in psutil.process_iter() if
                process.name() == "Festo MPS Distributing and Handling.exe"):
        os.kill(pid, signal.SIGTERM)
    print("Unity successfully closed")

