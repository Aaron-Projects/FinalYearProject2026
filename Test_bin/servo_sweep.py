import Jetson.GPIO as GPIO
import time

# Pin Definitions
SERVO_PIN = 32  # Adjust to your GPIO pin
# Setup
GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initialize PWM
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency for servo

def servo_angle(angle):
	if(angle == 0):
		duty_cycle = 2.5
	else:
		duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle
	pwm.ChangeDutyCycle(duty_cycle)
	time.sleep(0.02)  # Allow the servo to move

pwm.start(0)

def servo_sweep():
	try:
		print('starting-sweep')
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
	    pwm.stop()
	    GPIO.cleanup()

servo_sweep()
