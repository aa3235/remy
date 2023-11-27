import board
import time
import rotaryio
from math import pi

lenc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
renc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

ENCODER_TICKS_PER_REVOLUTION = 60
WHEELBASE_DIAMETER = 110
WHEEL_DIAMETER = 49.0 # mm

while True:
    MM_PER_TICK = pi * WHEEL_DIAMETER / ENCODER_TICKS_PER_REVOLUTION
    left_dist  = lenc.position * MM_PER_TICK
    right_dist = renc.position * MM_PER_TICK

    dist  = (left_dist + right_dist) / 2
    theta = (right_dist - left_dist) / WHEELBASE_DIAMETER

    print(dist, theta)
    time.sleep(0.05)