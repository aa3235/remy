import board
import busio
import time
import analogio
import pwmio
import digitalio

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

#motor1.duty_cycle = 65000
motor2.duty_cycle = 65000 #left wheel on junior, right on senior

running = False



