import board
import time
from math import pi
import digitalio
import rotaryio
import pwmio
import adafruit_motor.motor as motor



Ticks_Per_Turn = 60
Dist_Betwix_Wheels = 110
Wheel_Diameter = 49.0 # mm


# encoders
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

# motors
left_motor = motor.DCMotor(
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP0)
)
right_motor = motor.DCMotor(
    digitalio.DigitalInOut(board.GP4),
    digitalio.DigitalInOut(board.GP3)
)

left_motor.decay_mode = motor.SLOW_DECAY
right_motor.decay_mode = motor.SLOW_DECAY

# left_motor = pwmio.PWMOut(board.GP2, frequency = 1000)
# 
# left_motor_dir_1 = digitalio.DigitalInOut(board.GP1)
# left_motor_dir_1.direction = digitalio.Direction.OUTPUT
# left_motor_dir_2 = digitalio.DigitalInOut(board.GP0)
# left_motor_dir_2.direction = digitalio.Direction.OUTPUT
# 
# right_motor = pwmio.PWMOut(board.GP5, frequency = 1000)
# 
# right_motor_dir_1 = digitalio.DigitalInOut(board.GP4)
# right_motor_dir_1.direction = digitalio.Direction.OUTPUT
# right_motor_dir_2 = digitalio.DigitalInOut(board.GP3)
# right_motor_dir_2.direction = digitalio.Direction.OUTPUT
# 
# left_motor_dir_1.value = 0
# left_motor_dir_2.value = 1
# 
# right_motor_dir_1.value = 0
# right_motor_dir_2.value = 1



""" Main """

def limit(val):
    return min(1, max(val, -1))

if __name__ == "__main__":
    mm_per_tick = pi * Wheel_Diameter / Ticks_Per_Turn #gets distance travelled per tick of encoder

    while True:
        left_dist  = left_enc.position * mm_per_tick
        right_dist = right_enc.position * mm_per_tick

        dist  = (left_dist + right_dist) / 2
        theta = (right_dist - left_dist) / Dist_Betwix_Wheels

        Kp_angle = 0.1
        theta_target = 0

        e_angle = theta_target - theta
        start_angle = Kp_angle * e_angle

        left_motor.throttle, right_motor.throttle = (limit(1 - start_angle)), (limit(1 + start_angle))

        print(e_angle)

        time.sleep(0.05)