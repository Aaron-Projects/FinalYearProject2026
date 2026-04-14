# FinalYearProject2026  

READ ME FOR FINAL YEAR PROJECT!!!
-

-Main.py --> Main file  
- contains all needed definitions   
- Detects Motion -> Takes recordings of length = 8 seconds   
- Permanent live feed unless cancelled by user   
- 10 second cooldown between Recordings   
- function for activating recording via ultrasonic input  

-BACKUPMain.py --> Backup in case something happens to "main" file.  

-Videos:   
- Project_video.mov --> Footage of servo rotating to track detected objects   
- Recording_2026-03-18_08-25-09.avi --> Captured footage using "main.py" script to demonstrate    
									   object tracking capability, as well as timestamp   

-Test_bin:  
	*This folder contains old designs and smaller scripts used for experimentation,   
	most of which later implemented into the main file.* 

- countdown.py --> was used to infer logic for implementing cooldown on certain features

- Design 1, 1.5, 2, 3--> Previous versions of the main file

- greycam --> experimental version of a previous design, used to test how    
			ambient lighting affects the motion detection

- led.py --> activates a ring light attached to the camera/jetson  
			Planned to implement into main file,    
			would be activated when time is past sunset. But the ring light broke :(

- move.py --> uses a chosen integer (0-540) as a pretend measure of   
			 a hypothetical object's location relative to a camera frame.

- Tracking.py / obj_track1.py --> barebones object detection, mostly just used   
								 to check that the installed inference package/library works.

- servo_sweep.py --> sweeps servo from left to right and vice versa,   
					used in main when unsure of something being present   
					or when audio detected, but no object.   

- resetservo.py --> Resets servo if interuppted by sudden crash or otherwise not centered

Sources for inspiration and guidance:    
- Jetson hacks on github --> getting picamera to work with jetson https://github.com/JetsonHacksNano/CSI-Camera     
- dusty-nv on github --> Jetson inference https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera-2.md   

Prerequisite Libraries:   
-CV2   
-JETSON.GPIO   
-Jetson inference   
-Jetson utils   
-NUMPY   
-DATETIME   
-TIME   
