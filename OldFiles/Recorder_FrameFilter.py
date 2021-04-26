import numpy as np
import cv2
import mss
import mss.tools
import time
import imutils
import os.path
#----------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------Screen-Recording-Function----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

def screenRec(fps,sim_time,fourcc_avi,completeName1,completeName2,widths,heights,sizes,ofsets_h,ofsets_v):
    recording_start = time.time()
    # output videos
    output_avi = cv2.VideoWriter(completeName1, fourcc_avi, fps, sizes[0])
    output_avi2 = cv2.VideoWriter(completeName2, fourcc_avi, fps, sizes[1])

    frames = int(fps * sim_time)

    for i in range(frames):
        start = time.time()
        with mss.mss() as sct:
            region1 = {'top': ofsets_v[0], 'left': ofsets_h[0], 'width': widths[0], 'height': heights[0]}
            region2 = {'top': ofsets_v[1], 'left': ofsets_h[1], 'width': widths[1], 'height': heights[1]}
            img = sct.grab(region1)
            img2 = sct.grab(region2)

        # convert this image to numpy array
        img_np = np.array(img)
        img_np2 = np.array(img2)

        # reads colors as BGR
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        frame2 = cv2.cvtColor(img_np2, cv2.COLOR_BGR2RGB)

        # output the frame
        output_avi.write(frame)
        output_avi2.write(frame2)
        stop = time.time()
        duration = stop - start
        print(duration)
        dt = 1/fps - duration
        time.sleep(dt)

    recording_end = time.time()
    recording_duration = recording_end - recording_start
    err = (recording_duration - sim_time)/sim_time*100
    print("Loop excecuted in: "+str(recording_duration)+ " [s]")
    print("Which has a error of: "+str(err)+" [%] with the given simulation time")
    # close the window and release recording
    output_avi.release()
    output_avi2.release()

    # de-allocate any associated memory usage
    cv2.destroyAllWindows()

#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Frame-Filter-Function----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

def frameFilter(vs,completeName_filtered,min_area,fps,height,width,prod1_out_m):
    # setting parameters
    prod1 = [0]
    movement = [1]
    no_movement = [0]

    size = (width,height)

    prod1_out = cv2.VideoWriter(completeName_filtered, fourcc_avi, fps, size)

    # initializing variables and arrays
    prod1_frames = []
    prod1_matrix = [[],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []]
    firstFrame = None
    a = 0
    vid1 = 0
    row = 1
    firstIndex = 0
    secondIndex = 0
    thirdIndex = 0
    fourthIndex = 0
    fifthIndex = 0
    sixthIndex = 0
    seventhIndex = 0
    eightIndex = 0
    ninthIndex = 0
    tenthIndex = 0

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        succes, frame = vs.read()
        text = "Unoccupied"
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        # frame = cv2.resize(frame, size)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours

        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # appending the frames which have movement to the matrix
        if text == "Occupied":
            prod1_frames.append(frame)
            prod1_matrix[row-1].append(frame)
            prod1 = np.concatenate((prod1, movement))
        elif text == "Unoccupied":
            prod1 = np.concatenate((prod1, no_movement))

        # change this for the different simulations
        thresh_hold_frames = 5

        # setting the conditions on when to go to the next row in the frame matrix
        if prod1[len(prod1)-1] == 0:
            a += 1
            if a == thresh_hold_frames and len(prod1)-1 > thresh_hold_frames:
                vid1 += 1
                if firstIndex == 0:
                    firstIndex = len(prod1)-1
                    row = 2
                elif firstIndex > 0 and secondIndex == 0:
                    secondIndex = len(prod1)-1
                    row = 3
                elif secondIndex > 0 and thirdIndex == 0:
                    thirdIndex = len(prod1)-1
                    row = 4
                elif thirdIndex > 0 and fourthIndex == 0:
                    fourthIndex = len(prod1)-1
                    row = 5
                elif fourthIndex > 0 and fifthIndex == 0:
                    fifthIndex =len(prod1)-1
                    row = 6
                elif fifthIndex > 0 and sixthIndex == 0:
                    sixthIndex = len(prod1)-1
                    row = 7
                elif sixthIndex > 0 and seventhIndex == 0:
                    seventhIndex = len(prod1)-1
                    row = 8
                elif seventhIndex > 0 and eightIndex == 0:
                    eightIndex = len(prod1)-1
                    row = 9
                elif eightIndex > 0 and ninthIndex == 0:
                    ninthIndex = len(prod1)-1
                    # row = 10
                elif ninthIndex > 0 and tenthIndex == 0:
                    tenthIndex = len(prod1)-1
        elif prod1[len(prod1)-1] == 1:
            a = 0

        # draw the text and timestamp on the frame
        # cv2.putText(frame, "Simulation Status: {}".format(text), (10, 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        #             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # testing if no moving frames are missed
    moving_frames = np.count_nonzero(prod1==1)
    print("Counted moving frames: "+str(moving_frames))
    print("Moving frames in array: "+str(len(prod1_frames)))

    # making one video of all the moving frames
    for j in range(moving_frames):
        prod1_frame = cv2.cvtColor(prod1_frames[j], cv2.COLOR_BGR2RGB)
        prod1_out.write(prod1_frame)

    # making multiple videos for every seperate movement
    for rows in range(len(prod1_matrix)):
        for column in range(len(prod1_matrix[rows])):
            prod1_frame1 = cv2.cvtColor(prod1_matrix[rows][column], cv2.COLOR_BGR2RGB)
            prod1_out_m[rows].write(prod1_frame1)
        prod1_out_m[rows].release()

    print(prod1)

    # cleanup the camera and close any open windows
    prod1_out.release()
    vs.release()
    cv2.destroyAllWindows()

#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------General-Parameters-------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

# defining frame rate
fps = 10.0

# defining recording time
sim_time = 190.0

# defining the codec
fourcc_avi = cv2.VideoWriter_fourcc(*"XVID")

# directory for the scrap videos
video_name1 = "output1.avi"
video_name2 = "output2.avi"
save_path = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\scratch_video'
completeName1 = os.path.join(save_path,video_name1)
completeName2 = os.path.join(save_path,video_name2)
names = [completeName1, completeName2]

# directory for the filtered videos
# save_path_filtered_drop = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\dropoff\\correct'
# save_path_filtered_pick = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\pickup\\correct'
save_path_filtered_drop = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\dropoff\\incorrect'
save_path_filtered_pick = 'C:\\Users\\20182615\\Documents\\Jaar 3\\BEP\\EncodingDecoding\\filtered_videos\\pickup\\incorrect'
video_names_filtered = ["prod1_filtered.avi", "prod2_filtered.avi"]
save_path_filtered = [save_path_filtered_pick, save_path_filtered_drop]

# video specifications
widths = [306, 142]
heights = [416, 268]

sizes = [(widths[0],heights[0]),(widths[1],heights[1])]

ofsets_h = [2957, 3365]
ofsets_v = [117, 79]

# calling the screen recorder function
screenRec(fps, sim_time, fourcc_avi, completeName1,completeName2,widths,heights,sizes,ofsets_h,ofsets_v)

# setting the minimal area for detecting the moving object, higher means less noise
min_areas = [10000, 4000]

# making the video files for the trimmed an filtered videos
prod1_out_m1 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick45.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m2 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick46.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m3 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick47.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m4 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick48.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m5 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick49.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m6 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick50.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m7 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick51.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m8 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick52.avi"), fourcc_avi,fps,sizes[0])
prod1_out_m9 = cv2.VideoWriter(os.path.join(save_path_filtered_pick, "pick53.avi"), fourcc_avi,fps,sizes[0])
# prod1_out_m10 = cv2.VideoWriter(os.path.join(save_path, "10.avi"), fourcc_avi,fps,size)

prod1_out_m12 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop1.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m22 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop2.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m32 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop3.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m42 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop4.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m52 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop5.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m62 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop6.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m72 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop7.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m82 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop8.avi"), fourcc_avi,fps,sizes[1])
prod1_out_m92 = cv2.VideoWriter(os.path.join(save_path_filtered_drop, "drop9.avi"), fourcc_avi,fps,sizes[1])
# prod1_out_m10 = cv2.VideoWriter(os.path.join(save_path, "10.avi"), fourcc_avi,fps,size)

# putting the video files in a matrix for better handling
prod1_out_matrix1 = [prod1_out_m1, prod1_out_m2, prod1_out_m3,
               prod1_out_m4,prod1_out_m5,prod1_out_m6,
               prod1_out_m7,prod1_out_m8,prod1_out_m9]

prod1_out_matrix2 = [prod1_out_m12, prod1_out_m22, prod1_out_m32,
               prod1_out_m42,prod1_out_m52,prod1_out_m62,
               prod1_out_m72,prod1_out_m82,prod1_out_m92]

prod1_out_matrix = [prod1_out_matrix1, prod1_out_matrix2]


for i in range(len(video_names_filtered)):
#----------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Calling-of-Functions-----------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------#

    # video specific parameters
    # defining screen size
    width = widths[i-1]
    height = heights[i-1]

    # defining ofset
    ofset_h = ofsets_h[i-1]
    ofset_v = ofsets_v[i-1]

    # minimum area of moving object
    min_area = min_areas[i-1]

    # which video to take
    vs = cv2.VideoCapture(names[i-1])

    # file name of video
    video_name_filtered = video_names_filtered[i-1]
    completeName_filtered = os.path.join(save_path_filtered[i-1],video_name_filtered)

    # file name for trimmed videos
    prod1_out_m = prod1_out_matrix[i-1]

    # REMOVING the scratch videos from directory
    # os.remove(names[i-1])

    # calling the function
    frameFilter(vs,completeName_filtered,min_area,fps,height,width,prod1_out_m)


