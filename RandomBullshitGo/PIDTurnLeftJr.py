import board
import time
from math import pi

import digitalio
import rotaryio
import pwmio

time.sleep(10)

""" Constants """

Ticks_Per_Turn = 200
Dist_Betwix_Wheels = 70
Wheel_Diameter = 40.0 # mm


# encoders
left_enc = rotaryio.IncrementalEncoder(board.GP21, board.GP20)
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

# motors
right_motor = pwmio.PWMOut(board.GP2, frequency = 1000)

right_motor_dir_1 = digitalio.DigitalInOut(board.GP1)
right_motor_dir_1.direction = digitalio.Direction.OUTPUT
right_motor_dir_2 = digitalio.DigitalInOut(board.GP0)
right_motor_dir_2.direction = digitalio.Direction.OUTPUT

left_motor = pwmio.PWMOut(board.GP5, frequency = 1000)

left_motor_dir_1 = digitalio.DigitalInOut(board.GP4)
left_motor_dir_1.direction = digitalio.Direction.OUTPUT
left_motor_dir_2 = digitalio.DigitalInOut(board.GP3)
left_motor_dir_2.direction = digitalio.Direction.OUTPUT

right_motor_dir_1.value = 0
right_motor_dir_2.value = 1

left_motor_dir_1.value = 0
left_motor_dir_2.value = 1


""" Main """

def limit(val, min_val, max_val):
    return min(max_val, max(val, min_val))

# find dist and theta
def find_angle():
    mm_per_tick = pi * Wheel_Diameter / Ticks_Per_Turn

    right_dist  = right_enc.position * mm_per_tick
    left_dist = left_enc.position * mm_per_tick

    dist  = (right_dist + left_dist) / 2
    theta = (left_dist - right_dist) / Dist_Betwix_Wheels

    return dist, theta

# find correction and error terms for a target theta
error_angle_integral, error_angle_previous = 0, 0
def find_start_angle(theta, theta_target):
    Kp, Ki, Kd = 0.1, 0.005, 0.01

    global error_angle_integral, error_angle_previous
    error_angle = theta_target - theta

    # update I
    error_angle_integral += error_angle
    error_angle_integral = limit(error_angle_integral, -20, 20) # windup

    # update D
    error_angle_derivative = error_angle - error_angle_previous
    error_angle_previous  = error_angle

    start_angle = Kp * error_angle + Ki * error_angle_integral + Kd * error_angle_derivative
    return start_angle, error_angle

# find correction and error terms for a target distance
error_line_integral, error_line_previous = 0, 0
def find_start_line(dist, dist_target):
    Kp, Ki, Kd = 0.01, 0.0005, 0.005

    global error_line_integral, error_line_previous
    error_line = dist_target - dist

    # update I
    error_line_integral += error_line
    error_line_integral = limit(error_line_integral, -100, 100) # windup

    # update D
    error_line_derivative = error_line - error_line_previous
    error_line_previous  = error_line

    start_line= Kp * error_line + Ki * error_line_integral + Kd * error_line_derivative
    start_line = limit(start_line, -0.3, 0.3)
    return start_line, error_line

def run_control_loop(theta_target, dist_target):
    dist, theta = find_angle()
    start_angle, error_angle = find_start_angle(theta, theta_target)
    start_line, error_line = find_start_line(dist, dist_target)
    right_motor.duty_cycle, left_motor.duty_cycle = int(abs((limit(start_line - start_angle, -1, 1))) * 65535), int(abs((limit(start_line + start_angle, -1, 1))) * 65535)
    return error_angle, error_line

def reset_encoders():
    right_enc.position, left_enc.position = 0, 0

def reset_controls():
    global error_angle_integral, error_angle_previous, error_line_integral, error_line_previous
    error_angle_integral, error_angle_previous, error_line_integral, error_line_previous = 0, 0, 0, 0

def turn_right():
    reset_encoders()
    while abs(run_control_loop(pi/2, 0)[0]) > 0.05:
        time.sleep(0.02)
    reset_controls()
    right_motor.duty_cycle, left_motor.duty_cycle = 0, 0
if __name__ == "__main__":
    while True:
        turn_right()
        time.sleep(1)
