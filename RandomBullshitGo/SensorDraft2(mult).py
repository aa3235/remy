import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
import digitalio
import time


i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

ledL = digitalio.DigitalInOut(board.GP18)
ledL.direction = digitalio.Direction.OUTPUT
ledR = digitalio.DigitalInOut(board.GP19)
ledR.direction = digitalio.Direction.OUTPUT
mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Rsensor = adafruit_vl6180x.VL6180X(mux[5])
Fsensor = adafruit_vl6180x.VL6180X(mux[7])
Lsensor = adafruit_vl6180x.VL6180X(mux[6])

while True:

    print('R Range: {0}mm'.format(Rsensor.range))
    print('F Range: {0}mm'.format(Fsensor.range))
    print('L Range: {0}mm'.format(Lsensor.range))
    
    if Lsensor.range < 30:
        ledL.value = True
    else:
        ledL.value = False
        
    if Rsensor.range < 30:
        ledR.value = True
    else:
        ledR.value = False
        



