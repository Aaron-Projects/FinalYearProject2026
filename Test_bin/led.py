# This script was to control a lipsaroi ring light (IR) attached to the camera,
# unortubnately the light stopped working so this script was shelved
import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbers
LED_CTRL = 11             # GPIO pin connected to ring's GPIO

GPIO.setup(LED_CTRL, GPIO.OUT)

# Turn LEDs ON
GPIO.output(LED_CTRL, GPIO.HIGH)
time.sleep(5)

# Turn LEDs OFF
GPIO.output(LED_CTRL, GPIO.LOW)

GPIO.cleanup()
