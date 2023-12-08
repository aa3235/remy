import board
import time
from math import pi

import digitalio
import rotaryio
import pwmio
import adafruit_motor.motor as motor


lmot = motor.DCMotor(
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP0)
)
rmot = motor.DCMotor(
    digitalio.DigitalInOut(board.GP4),
    digitalio.DigitalInOut(board.GP3)
)
lmot.decay_mode = motor.SLOW_DECAY
rmot.decay_mode = motor.SLOW_DECAY

lmot.throttle = 0.8
rmot.throttle = 0.8