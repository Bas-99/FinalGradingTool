'''
    *************************************************************
    *                       Recorder.py                         *
    *************************************************************
'''

# ----------------------------
# Importing relevant libraries
# ----------------------------

import os
import numpy as np
import cv2
import mss
import mss.tools
import time

# --------------------------------------
# Definition of screen recorder function
# --------------------------------------

def screenRec(fps, sim_time, fourcc_avi, name, widths, heights, sizes, ofsets_h, ofsets_v):
    # output videos
    output_avi = cv2.VideoWriter(name, fourcc_avi, fps, sizes)

    frames = int(fps * sim_time)
    recording_start = time.time()
    for i in range(frames):
        start = time.time()
        with mss.mss() as sct:
            region1 = {'top': ofsets_v, 'left': ofsets_h, 'width': widths, 'height': heights}
            img = sct.grab(region1)

        # convert this image to numpy array
        img_np = np.array(img)

        # reads colors as BGR
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        # output the frame
        output_avi.write(frame)

        stop = time.time()
        loop_time = stop - start
        if loop_time < 1/fps:
            dt = 1/fps - loop_time
            time.sleep(dt)
        elif loop_time > 1/fps:
            print("CAUTION: loop is slower than the requested frame rate")
    recording_end = time.time()
    recording_duration = recording_end - recording_start
    err = (recording_duration - sim_time) / sim_time * 100
    print("screenRec executed in: " + str(recording_duration) + " seconds")
    print("Which has an error of: " + str(err) + " % with the given simulation time")

    # close the window and release recording
    output_avi.release()
    # output_avi2.release()

    # de-allocate any associated memory usage
    cv2.destroyAllWindows()

# -----------------------------------------------
# Definition of reallocater and resizing function
# -----------------------------------------------

def frameFilter(name, fps, height, width, save_path_test, fourcc_avi, fileName, assignments):
    # setting parameters
    all_frames = []

    size = (width, height)

    vs = cv2.VideoCapture(name)

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied text
        succes, frame = vs.read()

        # if the frame could not be grabbed, then we have reached the end of the video
        if frame is None:
            break

        resized = cv2.resize(frame, (64, 64))
        all_frames.append(resized)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    prod_out = cv2.VideoWriter(os.path.join(save_path_test, fileName + assignments + ".avi"),
                               fourcc_avi, fps, (64, 64))

    for frame in all_frames:
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        prod_out.write(frame1)

    prod_out.release()
    vs.release()
    cv2.destroyAllWindows()
