import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
import time
import analogio
import pwmio
import digitalio

i2c = busio.I2C(board.GP15, board.GP14)
mux = adafruit_tca9548a.TCA8548A(i2c)

Lsensor = adafruit_vl6180x.VL6180X(mux[7])
Fsensor = adafruit_vl6180x.VL6180X(mux[0])
Rsensor = adafruit_vl6180x.VL6180X(mux[3])

print('L Range: {0}mm'.format(Lsensor.range))
print('F Range: {0}mm'.format(Fsensor.range))
print('R Range: {0}mm'.format(Rsensor.range))

motor1.duty_cycle = 20000  #Left Motor
motor2.duty_cycle = 20000  #Right Motor

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

#Directions

def forward:
	d1.value = 1
	d2.value = 0
	d3.value = 1
	d4.value = 0

def backward:
	d1.value = 0
	d2.value = 1
	d3.value = 0
	d4.value = 1

def left:
	d1.value = 0
	d2.value = 1
	d3.value = 1
	d4.value = 0

def right:
	d1.value = 1
	d2.value = 0
	d3.value = 0
	d4.value = 1

def stop:
	d1.value = 0
	d2.value = 0
	d3.value = 0
	d4.value = 0

def leftadjust:
	motor1.duty_cycle = motor1.duty_cycle + 2000
	motor2.duty_cycle = motor1.duty_cycle - 2000

def revertleftadjust:
	motor1.duty_cycle = motor1.duty_cycle - 2000
	motor2.duty_cycle = motor1.duty_cycle + 2000

def rightadjust:
	motor1.duty_cycle = motor1.duty_cycle - 2000
	motor2.duty_cycle = motor1.duty_cycle + 2000

def revertrightadjust:
	motor1.duty_cycle = motor1.duty_cycle + 2000
	motor2.duty_cycle = motor1.duty_cycle - 2000

runtime = True

try:
	while runtime = True:
		forwards()
		if Fsensor.range() < 30:
			stop()
		if Lsensor.range() > 40:
			stop()
			left()
			time.sleep(0.5)
			forwards()
			runtime == False
		if Rsensor.range() > 40:
			stop()
			right()
			time.sleep(0.5)
			forwards()
			runtime == False

	if runtime = False:
		forwards()
		time.sleep(1)
		runtime == True