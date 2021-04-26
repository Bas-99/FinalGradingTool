import numpy as np
import cv2
import mss
import mss.tools
import time
import imutils
import os.path
import multiprocessing
import threading
from multiprocessing import Pool
#----------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------Screen-Recording-Function----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

def screenRec(fps,sim_time,fourcc_avi,name,widths,heights,sizes,ofsets_h,ofsets_v):
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

#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Frame-Filter-Function----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

def frameFilter(name,min_area,fps,height,width,save_path_test,fourcc_avi,fileName):
    # setting parameters
    prod1 = [0]
    movement = [1]
    no_movement = [0]

    size = (width,height)

    vs = cv2.VideoCapture(name)

    # initializing variables and arrays
    prod1_frames = []
    test_frame_arr = []
    firstFrame = None

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied text
        succes, frame = vs.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end of the video
        if frame is None:
            break

        # convert the frame to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue
            text = "Occupied"

        # appending the frames which have movement to the matrix
        if text == "Occupied":
            prod1 = np.concatenate((prod1, movement))
        elif text == "Unoccupied":
            prod1 = np.concatenate((prod1, no_movement))

        test_frame_arr.append(frame)

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    arr_row = 1

    # testing if no moving frames are missed
    moving_frames = np.count_nonzero(prod1==1)
    # print("Counted moving frames: "+str(moving_frames))

    prod_out = cv2.VideoWriter(os.path.join(save_path_test, fileName + str(arr_row) + ".avi"), fourcc_avi, fps, size)
    for a in range(len(prod1)):
        if prod1[a] == 1:
            prod1_frame1 = cv2.cvtColor(test_frame_arr[a-1], cv2.COLOR_BGR2RGB)
            prod_out.write(prod1_frame1)
        elif prod1[a] == 0 and prod1[a-1] == 1 and a > 1:
            prod_out.release()
            # print("Video: "+str(arr_row)+" is ready")
            arr_row += 1
            prod_out = cv2.VideoWriter(os.path.join(save_path_test, fileName + str(arr_row) + ".avi"), fourcc_avi, fps,
                                       size)

    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()

#----------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------Video-Parameters-------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
# first values are for prod 1, second values are for drop off, third values are for vacuum waiting, fourth values are
# for prod 3

# defining frame rate
fps = 10.0

# defining recording time
sim_time = 180.0

# defining the codec
fourcc_avi = cv2.VideoWriter_fourcc(*"XVID")

# video specifications
widths = [306, 142, 300, 92]
heights = [416, 268, 99, 126]

sizes = [(widths[0],heights[0]),(widths[1],heights[1]),(widths[2],heights[2]),(widths[3],heights[3])]

ofsets_h = [2957, 3365, 2097, 2322]
ofsets_v = [117, 79, 588, 116]

# setting the minimal area for detecting the moving object, higher means less noise
min_areas = [10000, 4000, 2000, 2000]

#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------Directory-Scratch-Videos---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

# directory for the scrap videos
video_name1 = "prod1.avi"
video_name2 = "dropoff.avi"
video_name3 = "vacuum.avi"
video_name4 = "prod3.avi"
save_path = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\scratch_video'
completeName1 = os.path.join(save_path,video_name1)
completeName2 = os.path.join(save_path,video_name2)
completeName3 = os.path.join(save_path,video_name3)
completeName4 = os.path.join(save_path,video_name4)
names = [completeName1, completeName2, completeName3, completeName4]

#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------Directory-Filtered-Videos--------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

# directory for the filtered videos (choose in if placed in correct or incorrect directory)
# save_path_filtered_drop = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\dropoff\\correct'
# save_path_filtered_pick = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\pickup\\correct'
save_path_filtered_drop = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\test1'
save_path_filtered_pick = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\test2'
save_path_filtered = [save_path_filtered_pick, save_path_filtered_drop]
vid_names = ["prod1", "dropoff", "vacuum", "prod3"]

#----------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------Calling-of-Screen-Recorder-------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
inputs = [(fps, sim_time, fourcc_avi, names[0], widths[0], heights[0], sizes[0], ofsets_h[0], ofsets_v[0]),
          (fps, sim_time, fourcc_avi, names[1], widths[1], heights[1], sizes[1], ofsets_h[1], ofsets_v[1]),
          (fps, sim_time, fourcc_avi, names[2], widths[2], heights[2], sizes[2], ofsets_h[2], ofsets_v[2]),
          (fps, sim_time, fourcc_avi, names[3], widths[3], heights[3], sizes[3], ofsets_h[3], ofsets_v[3])]

processes = []

if __name__ == '__main__':
    for input in inputs:
        p = multiprocessing.Process(target=screenRec, args=input)
        p.start()
        processes.append(p)
    for process in processes:
        process.join()

#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Calling-of-Frame-Filter--------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
inputs = [(names[0], min_areas[0], fps, heights[0], widths[0], save_path_filtered[0], fourcc_avi, vid_names[0]),
          (names[1], min_areas[1], fps, heights[1], widths[1], save_path_filtered[0], fourcc_avi, vid_names[1]),
          (names[2], min_areas[2], fps, heights[2], widths[2], save_path_filtered[0], fourcc_avi, vid_names[2]),
          (names[3], min_areas[3], fps, heights[3], widths[3], save_path_filtered[0], fourcc_avi, vid_names[3])]

threads = []
processes = []
start = time.time()

if __name__ == '__main__':
    # with Pool(4) as p:
    #     results = p.starmap(frameFilter, inputs)
    for input in inputs:
        t = threading.Thread(target=frameFilter,args=input)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()

end = time.time()
duration = end - start
print("Filtering videos finished in: " + str(duration) + " seconds")





