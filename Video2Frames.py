#----------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------Video2Frames.py-------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
# This file contains two function, one for general frame extraction from a .avi file and one for creating valid data   #
# to feed into the ML models.                                                                                          #
#----------------------------------------------------------------------------------------------------------------------#

import cv2
import numpy as np
import os

img_height, img_width = 64, 64

classes = ["incorrect", "correct"]

# this function will convert video files to frame lists
def frames_extraction(video_path,seq_len):
    frames_list = []

    vidObj = cv2.VideoCapture(video_path)
    # Used as counter variable
    count = 1

    while count <= seq_len:

        success, image = vidObj.read()
        if success:
            image = cv2.resize(image, (img_height, img_width))
            frames_list.append(image)
            count += 1
        else:
            print("Defected frame")
            break

    return frames_list

# this function will use frames_extraction() to loop over all
# files in the given directory and store the data in X
def create_data(input_dir,seq_len):
    X = []

    files_list = os.listdir(input_dir)

    for f in files_list:
        frames = frames_extraction(os.path.join(input_dir, f),seq_len)
        if len(frames) == seq_len:
            X.append(frames)

    X = np.asarray(X)
    return X
