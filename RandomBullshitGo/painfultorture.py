import board
import time
import analogio
import digitalio
import busio
import pwmio
import adafruit_tca9548a
import adafruit_vl6180x
import rotaryio

runtime = True
stage = 1
# Sensor SETUP

i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA
mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Rsensor = adafruit_vl6180x.VL6180X(mux[5])
Fsensor = adafruit_vl6180x.VL6180X(mux[7])
Lsensor = adafruit_vl6180x.VL6180X(mux[6])

print('R Range: {0}mm'.format(Rsensor.range))
print('F Range: {0}mm'.format(Fsensor.range))
print('L Range: {0}mm'.format(Lsensor.range))

# Encoder SETUP

left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

#MOTOR SETUP

motorR = pwmio.PWMOut(board.GP2, frequency = 1000)

d1 = digitalio.DigitalInOut(board.GP1)
d1.direction = digitalio.Direction.OUTPUT
d2 = digitalio.DigitalInOut(board.GP0)
d2.direction = digitalio.Direction.OUTPUT

motorL = pwmio.PWMOut(board.GP5, frequency = 1000)

d3 = digitalio.DigitalInOut(board.GP4)
d3.direction = digitalio.Direction.OUTPUT
d4 = digitalio.DigitalInOut(board.GP3)
d4.direction = digitalio.Direction.OUTPUT

d1.value = 0
d2.value = 1

d3.value = 0
d4.value = 1

runtime = True

def turnspeed():
    motorR.duty_cycle = 20000
    motorL.duty_cycle = 20000

def motorflat():
    motorR.duty_cycle = 0
    motorL.duty_cycle = 0

def forward():
    d1.value = 0
    d2.value = 1

    d3.value = 0
    d4.value = 1
    timeout = time.time() + 0.5
    while time.time() < timeout:
        
        if left_enc.position > right_enc.position:
            motorR.duty_cycle = 30000
        elif right_enc.position > left_enc.position:
            motorR.duty_cycle = 0
            motorL.duty_cycle = 30000
        else:
            motorR.duty_cycle = 30000
            motorL.duty_cycle = 30000
            error = 30 - Lsensor.range
            doof = error * 100
            motorR.duty_cycle = 30000 - doof
            motorL.duty_cycle = 30000 + doof

def smallforward():
    d1.value = 0
    d2.value = 1

    d3.value = 0
    d4.value = 1
    timeout = time.time() + 0.3
    while time.time() < timeout:
        
        if left_enc.position > right_enc.position and error != 0:
            motorR.duty_cycle = 30000
        elif right_enc.position > left_enc.position and error != 0:
            motorR.duty_cycle = 0
            motorL.duty_cycle = 30000
        else:
            motorR.duty_cycle = 30000
            motorL.duty_cycle = 30000
            error = 30 - Lsensor.range
            doof = error * 100
            motorR.duty_cycle = 30000 - doof
            motorL.duty_cycle = 30000 + doof
    
def buffer():
    forward()
    time.sleep(1)
    motorflat()
    
def rightturn():
    motorflat()
    d1.value = 1
    d2.value = 0

    d3.value = 0
    d4.value = 1
    turnspeed()
    time.sleep(0.5)
    motorflat()


def leftturn():
    motorflat()
    d1.value = 0
    d2.value = 1

    d3.value = 1
    d4.value = 0
    turnspeed()
    time.sleep(0.5)
    motorflat()

def sensorread():
    print('R Range: {0}mm'.format(Rsensor.range))
    print('F Range: {0}mm'.format(Fsensor.range))
    print('L Range: {0}mm'.format(Lsensor.range))

    
def smallbuffer():
    forward()
    time.sleep(0.3)
    motorflat()

while runtime == True:
    forward()
    if Lsensor.range >= 70:
        motorflat()
        time.sleep(0.5)
        smallforward()
        time.sleep(0.5)
        leftturn()
        time.sleep(0.5)
        smallforward()
    elif Fsensor.range <= 50:
        motorflat()
        if Lsensor.range >= 70:
            time.sleep(0.5)
            leftturn()
            time.sleep(0.5)
            smallforward()
        elif Rsensor.range >= 70:
            time.sleep(0.5)
            rightturn()
            time.sleep(0.5)
            smallforward()
        else:
            motorflat()
            rightturn()
            time.sleep(0.5)
            rightturn()
            time.sleep(0.5)
