import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
import time
import analogio
import pwmio
import digitalio

#sensor time
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Lsensor = adafruit_vl6180x.VL6180X(mux[7])
Fsensor = adafruit_vl6180x.VL6180X(mux[0])
Rsensor = adafruit_vl6180x.VL6180X(mux[3])

print('L Range: {0}mm'.format(Lsensor.range))
print('F Range: {0}mm'.format(Fsensor.range))
print('R Range: {0}mm'.format(Rsensor.range))
#wheel time
motor1 = pwmio.PWMOut(board.GP2, frequency = 1000)

d1 = digitalio.DigitalInOut(board.GP1)
d1.direction = digitalio.Direction.OUTPUT
d2 = digitalio.DigitalInOut(board.GP0)
d2.direction = digitalio.Direction.OUTPUT

motor2 = pwmio.PWMOut(board.GP5, frequency = 1000)

d3 = digitalio.DigitalInOut(board.GP4)
d3.direction = digitalio.Direction.OUTPUT
d4 = digitalio.DigitalInOut(board.GP3)
d4.direction = digitalio.Direction.OUTPUT

d1.value = 0
d2.value = 1

d3.value = 0
d4.value = 1

motor1.duty_cycle = 10000  #Left Motor
motor2.duty_cycle = 10000  #Right Motor



running = False
while True:
    time.sleep(0.1)
    print('F Range: {0}mm'.format(Fsensor.range))


    if Fsensor.range < 70:
        motor1.duty_cycle = 0
        motor2.duty_cycle = 0
    else:
        motor1.duty_cycle = 30000
        motor2.duty_cycle = 30000