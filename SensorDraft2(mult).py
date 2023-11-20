import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Rsensor = adafruit_vl6180x.VL6180X(mux[7])
Fsensor = adafruit_vl6180x.VL6180X(mux[0])
Lsensor = adafruit_vl6180x.VL6180X(mux[3])

print('R Range: {0}mm'.format(Lsensor.range))
print('F Range: {0}mm'.format(Fsensor.range))
print('L Range: {0}mm'.format(Rsensor.range))
