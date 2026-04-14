#this module served as a way to test thtat the servo used actually works,
#giving a reference for how it' move during an actaul use case.

import Jetson.GPIO as GPIO
import time
# Servo setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

pwm = GPIO.PWM(32, 50)
pwm.start(7.5)
def rotate_servo(x):
	print(f"object at x: {x}")
	if(225 <= x <= 315):
		print("subject in target range!")
	else:
		if(x<225):
			degree = ((270-x)/18)+2.5
		elif(x>315):
			degree = ((x-270)/18)+2.5
		
		
		pwm.ChangeDutyCycle(degree)
		time.sleep(0.2)  # Allow the servo to move
		pwm.ChangeDutyCycle(0)
		time.sleep(0.2)  # Allow the servo to move

# Example usage
rotate_servo(270)
time.sleep(1)
pwm.ChangeDutyCycle(7.5)
pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()
