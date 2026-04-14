import jetson_utils
import cv2
import numpy as np
camera = jetson_utils.videoSource("csi://0?mode=3&fps=30?flip-method=2")

prev_gray = None
motion_cooldown = 0
servo_cooldown = 0
object_x = 0

while(True):
	frame = camera.Capture()
	if(frame is None):
		continue
	
	#frame = jetson_utils.cudaAllocMapped(width=frame.width, height=frame.height, format=frame.format)
	#frame = cv2.rotate(jetson_utils.cudaToNumpy(frame), cv2.ROTATE_90_COUNTERCLOCKWISE)
	#frame = jetson_utils.cudaFromNumpy(frame)
	
	jetson_utils.cudaDeviceSynchronize()

	# Create small grayscale copy for motion detection (CPU)
	try:
		img_small = jetson_utils.cudaToNumpy(frame)
		img_small = cv2.cvtColor(img_small, cv2.COLOR_RGBA2BGR)
		img_small = cv2.resize(img_small, (320, 240))
		small_gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
	except:
		print("Error: could convert image for motion detection")
	# Motion detection
	#prev_gray, motion = motion_detect(prev_gray, small_gray)


	# Draw box around detected object
	img_live = jetson_utils.cudaToNumpy(frame)
	img_live = cv2.cvtColor(img_live, cv2.COLOR_RGBA2BGR)
	img_live = cv2.resize(img_live, (960, 540))

	# Show live feed
	cv2.imshow("Live Camera", img_live)
	

	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

del camera
print("Program terminated.")
