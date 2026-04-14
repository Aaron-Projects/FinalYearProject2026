*************************************************
*						*
*	READ ME FOR FINAL YEAR PROJECT!!!	*
*						*
*************************************************
 
For Working On Code:
-To Run Code, Must Set Directory To File Directory: $ cd /home/*<USER>*/Desktop/*<FOLDERNAME>*
-To Execute A Python File: python filename.py
-To Install A Package Return To Normal Directory ($ cd if already set elsewhere),
	then use "pip3" not "pip"
 
FYP folder:
- README.txt 

-Main.py --> Main file
	- contains all needed definitions
	- Detects Motion -> Takes recordings of length = 8 seconds
	- Permanent live feed unless cancelled by user
	- 10 second cooldown between Recordings
	
-BACKUPMain.py --> Bakcup in case something happens to "main" file.

-Test_bin:
	-- This folder contains old designs and smaller scripts used --
	-- for experimentation, most of which later implemented into --
	-- 			the main file.			     --
	
	-countdown.py --> used to infer logic for implementing cooldown on 
			  certain features
			  
	-Design1, 1.5, 2, 3--> Previous versions of the main file
	
	-greycam --> experimental version of a previous design, used
		   to test how ambient lighting affects the motion detection
		   
	-led.py --> activates a ring light attached to the camera/jetson
		  Planned to implement into main file, would be activated when
		  time is past sunset. But the ring light broke :(
	-move.py --> uses a chosen integer (0-540) as a pretend measure of a hypothetical 
		   object's location relative to a camera frame.
		   
	-Tracking.py / obj_track1.py --> barebones object detection, mostly just used to check 
			 that the installed inference package/library works.
			 
	-servo_sweep.py --> sweeps servo from left to right and vice versa, used in main 
			 when unsure of something being present or when audio detected,
			 but no object.
			 
To ADD:
-Script for taking input of UltraSonic sensor and activating camera
 
Sources for inspiration and guidance:
-Jetson hacks on github --> getting picamera to work with jetson
	https://github.com/JetsonHacksNano/CSI-Camera
-dusty-nv on github --> Jetson inference
	https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera-2.md
	
	
Prerequisite Libraries:
-CV2
-JETSON.GPIO
-Jetson inference
-Jetson utils
-NUMPY
-DATETIME
-TIME
-PIP(3)
