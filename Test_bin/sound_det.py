import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1_x_15.analog_in import AnalogIn
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
#takes input from A0 on ads1115
chan = AnalogIn(ads, ADS.P0)

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)

