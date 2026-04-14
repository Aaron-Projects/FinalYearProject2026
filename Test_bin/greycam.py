#motion_detect
import cv2
import numpy as np
import time
import datetime

#Makes the jetson work alongside a raspberry pi camera, must be called when creating a capture
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=2,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (#Gives the conditions of the camera, can be selectively edited if so desired
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

#Begins recording input to camera + stores it
def record(rec_start, videoName, cap):
	loop_time = time.time() - rec_start
	frame_rec_count = 0
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter(videoName,fourcc, 30.0, (960, 540)) #640, 480, if code fucked
	try: # Checks for if recording is possible
		while(frame_rec_count<240): #Frame Rate of 30fps --> 240 frames = 8 seconds
			print("Recording...", loop_time)
			ret, rec_frame = cap.read()
			rec_frame = cv2.putText(rec_frame, str(datetime.datetime.now()), (20,520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_8)
			cv2.imshow('Recording',rec_frame)
			out.write(rec_frame)
			frame_rec_count = frame_rec_count + 1
			if(cv2.waitKey(1) & 0xFF == ord('q')):
				print("Recording Process stopped at:", loop_time)
				break
			else:
				continue
		return 0
	except: #handles any issues where recording not possible
		print("Error: Could not begin recording\n")
		return 1
			
def LiveCam():
	#Uses the datetime library to assign the videoname as the date+time of recording
	#Makes organisaton easier and provides multiple categories to sort footage

	TimeOfRecording = str(datetime.datetime.now())
	videoName = ("VideoFile_"+TimeOfRecording+"_"+".avi")

	#Calls function to display input to camera
	try:
		cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
	except:
		print("Error: Unable to locate camera")
	#Initial data
	last_mean = 0
	footage = 0
	start = time.time()
	cooldown_time = 20.00 #Dictates time (s) before another video can be filmed
	rec_next = 0
	Cooldown = True
	LED_PIN = 11



	while(True):
		loop_time = round((time.time() - start), 2)
		
		loop_time_text = str(loop_time) # displays the current time (as camara activated)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LED_PIN, GPIO.OUT) #sets the LED ring as active
		GPIO.output(LED_PIN, GPIO.HIGH)
		
		ret, frame = cap.read()
		#add date/timestamp to footage & name to window
		frame = cv2.putText(frame, str(datetime.datetime.now()), (20,520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_8)
		cv2.imshow('Motion Detecting Software',frame)
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		result = np.abs(np.mean(gray) - last_mean)
		cv2.imshow('greyscale',gray) #experimental line to see how ambient lighting affects motion detection
		print(result, loop_time)
		last_mean= np.mean(gray)
		
		# Camera always detects motion on startup due to how the calculations work
		# This stops immediate recording
		if(loop_time <= 1):
			continue
		else:
			# 'result' is used as a measure of sensitivity 
			#FURTHER EXPERIMENTATION REQUIRED FOR DISTANCES
			if(loop_time >= rec_next):
				Cooldown = True
			if((result > 0.45) and (Cooldown==True)):	
				print("Motion detected!", loop_time)
				try:
					rec_next = loop_time + cooldown_time
					#footage = record(loop_time, videoName, cap)
					Cooldown = False
					continue
				except:
					print("Error: recording function not callable\n")
			if(cv2.waitKey(1) & 0xFF == ord('q') or footage==1):
				print("Process Stopped by user\n")
				break
			else:
				continue
	return cap
				
def main():
	
	Camera = LiveCam()
 
	Camera.release()
	cv2.destroyAllWindows()
	
if __name__== "__main__":
	main()

