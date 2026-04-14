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
time.sleep(0.5)
pwm.stop()
