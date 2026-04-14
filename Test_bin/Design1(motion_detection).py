#motion_detection
#this was the very first iteration of the design, using purely motion detection
#This design became the bassi for all future version of the software,
#using open cv for the streaming and file creation (conserving cpu/gpu power), and
#taking the mean of a frame for motion detection, which would begin the recording
import cv2
import numpy as np
import time
import datetime
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
#Uses the datetime library to assign the videoname as the date+time of recording
#Makes organisaton easier and prvides multiple categories to aort
TimeOfRecording = str(datetime.datetime.now())
videoName = ("VideoFile_"+TimeOfRecording+"_"+".avi")
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
last_mean = 0
detected_motion = False
frame_rec_count = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(videoName,fourcc, 30.0, (960, 540)) 
start = time.time()
while(True):
	loop_time = str(time.time() - start)
	ret, frame = cap.read()
	#add date/timestamp to footage & name to window
	frame = cv2.putText(frame, str(datetime.datetime.now()), (20,520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_8)
	cv2.imshow('Motion Detecting Software',frame)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	result = np.abs(np.mean(gray) - last_mean)
	print(result, loop_time)
	last_mean= np.mean(gray)
	print(result, loop_time)
	# 'result' is used as a measure of sensitivity 
#FURTHER EXPERIMENTATION REQUIRED FOR DISTANCES
	if(result > 0.15):
		print("Motion detected!", loop_time)
		print("Started recording.", loop_time)
		detected_motion = True
	if(detected_motion):
		out.write(frame)
		frame_rec_count = frame_rec_count + 1
	if(cv2.waitKey(1) & 0xFF == ord('q')) or frame_rec_count == 200:
		break
	else:
		continue
 
cap.release()
cv2.destroyAllWindows()
