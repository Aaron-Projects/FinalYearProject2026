#Main program for Final Year Project
#Contains all modules needed

#necessary libraries
import jetson_inference
import jetson_utils
import Jetson.GPIO as GPIO
import cv2
import numpy as np
import datetime
import time
#import Adafruit_ADS1x15
#adc = Adafruit_ADS1x15.ADS1115()

#setting up servos

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
pwm = GPIO.PWM(32, 50)
pwm.start(7.5)
global current_duty
current_duty = 2.5
#rotating servo to center subject in frame, 
#uses coordinates from box around object
def rotate_servo(x):
	if(x>=450 and x <= 510):
		print("subject in target range!")
		return 0
	else:
		if(x<480):
			degree = ((480-x)/180)+2.5
		elif(x>480):
			degree = ((x-480)/180)+2.5
		degree = max(2.5, min(degree, 12.5))  # prevents servo going too far

		pwm.ChangeDutyCycle(degree)
		time.sleep(0.05)
		pwm.ChangeDutyCycle(0)
		current_duty = degree
		
		pwm.ChangeDutyCycle(degree)
		time.sleep(0.2)  # Allow the servo to move
		
		time.sleep(0.2)  # Allow the servo to move
		return 0
		
def servo_angle(angle):
	if(angle == 0):
		duty_cycle = 2.5
	else:
		duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle
	pwm.ChangeDutyCycle(duty_cycle)
	time.sleep(0.02)  # Allow the servo to move



def servo_sweep():
	try:
		print('starting sweep')
		#0 to 180 degrees
		for angle in range(0, 181):
			servo_angle(angle)
			time.sleep(0.01) 

		#180 to 0 degrees
		for angle in range(180, -1, -1):
			servo_angle(angle)
			time.sleep(0.01)
		
		print('Finished sweep')

	except KeyboardInterrupt:
		pwm.ChangeDutyCycle(7.5)	
		
def read_voltage():
	# Read the ADC channel 0
	value = adc.read_adc(0, gain=1)
	# Convert raw value to voltage (ADS1115 is 16-bit)
	voltage = value * (4.096 / 32767.0)
	return voltage
	
#uses means of frames to decide if motion has occured
def motion_detect(prev_gray, small_gray):
	if(prev_gray is None):
		return small_gray, False
	diff = abs(np.mean(small_gray) - np.mean(prev_gray))
	return small_gray, diff > 5.0 # Number determines threshold for motion detection,
					# can be changed depending on desired sensitivity
	
# If motion is detected, this function is called,
# Records 8 seconds from camera and save as AVI w/ timestamp.
def record_video(net, camera):
	frame_count = 0
	object_x= 0
	servo_cooldown = 0
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	#timestamp as filename, makes organisation easier 
	filename = f"Recording_{timestamp}.avi"
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter(filename, fourcc, 30, (960, 540))
	print(f"Recording started: {filename}")
	while(frame_count<=240):
		frame = camera.Capture()
		if(frame is None):
			continue

		jetson_utils.cudaDeviceSynchronize()

		# Run detection on CUDA frame directly
		detections = net.Detect(frame)

		# Convert to NumPy only for saving and drawing
		img = jetson_utils.cudaToNumpy(frame)
		img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
		img = cv2.resize(img, (960, 540))

		# Draw detections
		for d in detections:
			left, top, right, bottom = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
			cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
			object_x = int(round((d.Left + d.Right) / 2))  # update object x-coordinate
		print("object at x: ", object_x)
		if(time.time() > servo_cooldown):
			rotate_servo(object_x)
			servo_cooldown = (time.time() + 0.5) # gives servo time to move
		# Add timestamp at bottom left
		img = cv2.putText(img,
			datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			(10, 240),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.5,
			(255, 255, 255),
			2)
		
		out.write(img)
		# Optional: show recording feed
		cv2.imshow("Recording", img)
		frame_count+=1
		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break

	out.release()
	cv2.destroyWindow("Recording")
	print("Recording finished")

# Shows a live feed from the camera to the screen
def live_cam():
	try:
		
		camera = jetson_utils.videoSource("csi://0?mode=0&fps=30?flip-method=3")
		#display = jetson_utils.videoOutput("display://0")  # Jetson display
		net = jetson_inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

		prev_gray = None
		motion_cooldown = 0
		servo_cooldown = 0
		object_x = 0
		
		while(True):
			time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			frame = camera.Capture()
			if(frame is None):
				continue
			
			jetson_utils.cudaDeviceSynchronize()
			sweep = 0.0
			#sweep = read_voltage()
			if(sweep >  0.1):
				sweep_servo()
				time.wait(0.2)
			# Create small grayscale copy for motion detection (CPU)
			try:
				img_small = jetson_utils.cudaToNumpy(frame)
				img_small = cv2.cvtColor(img_small, cv2.COLOR_RGBA2BGR)
				img_small = cv2.resize(img_small, (320, 240)) #uses smaller frame size to make calculations less demanding
				small_gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
			except:
				print("Error: could convert image for motion detection")
			# Motion detection
			prev_gray, motion = motion_detect(prev_gray, small_gray)
			
			# Object detection on CUDA frame (cant work on cv2)
			detections = net.Detect(frame)	

			# Draw box around detected object
			img_live = jetson_utils.cudaToNumpy(frame)
			img_live = cv2.cvtColor(img_live, cv2.COLOR_RGBA2BGR)
			img_live = cv2.resize(img_live, (960, 540))

			for d in detections:
				left, top, right, bottom = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
				cv2.rectangle(img_live, (left, top), (right, bottom), (0, 255, 0), 2)
				object_x = int(round((d.Left + d.Right) / 2))  # update object x-coordinate
			print("object at x: ", object_x)
			if(time.time() > servo_cooldown):
				rotate_servo(object_x)
				servo_cooldown = (time.time() + 0.5)
			# Add timestamp at bottom left
			cv2.putText(img_live,
				time_stamp,
				(10, 240),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5,
				(255, 255, 255),
				2)

			# Show live feed
			cv2.imshow("Live Camera", img_live)
			
			# Check cooldown and record if motion detected
			if((motion) and (time.time() > motion_cooldown)):
				print("Motion detected! Starting recording...")
				cv2.destroyWindow("Live Camera")
				record_video(net, camera)
				motion_cooldown = time.time() + 18  # 10-second cooldown (8 seconds = recording length)
				prev_gray = None  # reset previous frame after recording
				
			if(cv2.waitKey(1) & 0xFF == ord('q')):
				break

	except KeyboardInterrupt:
		print("Process Ended by user")
	finally:
		del camera
		time.sleep(0.5)
		pwm.ChangeDutyCycle(7.5)
		pwm.stop()
		GPIO.cleanup()
		cv2.destroyAllWindows()
		print("Program terminated.")
		
		
def main():
	live_cam()
	
if __name__ == "__main__":
	main()
