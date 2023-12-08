import board
import time
from math import pi

import rotaryio
import pwmio
import analogio
import digitalio

import busio
import adafruit_tca9548a
import adafruit_vl6180x



""" Constants """
Ticks_Per_Turn = 200
Dist_Betwix_Wheels = 70
Wheel_Diameter = 40.0 # mm

#leds
ledL = digitalio.DigitalInOut(board.GP18)
ledL.direction = digitalio.Direction.OUTPUT
ledR = digitalio.DigitalInOut(board.GP19)
ledR.direction = digitalio.Direction.OUTPUT

#sensors
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Rsensor = adafruit_vl6180x.VL6180X(mux[5])
Fsensor = adafruit_vl6180x.VL6180X(mux[7])
Lsensor = adafruit_vl6180x.VL6180X(mux[6])

#print('R Range: {0}mm'.format(Rsensor.range))
#print('F Range: {0}mm'.format(Fsensor.range))
#print('L Range: {0}mm'.format(Lsensor.range))

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

# get dist and theta
def get_odometry():
    mm_per_tick = pi * Wheel_Diameter / Ticks_Per_Turn

    left_dist  = left_enc.position * mm_per_tick
    right_dist = right_enc.position * mm_per_tick

    dist  = (left_dist + right_dist) / 2
    theta = (right_dist - left_dist) / Dist_Betwix_Wheels

    return dist, theta

# get correction and error terms for a target theta
def get_start_angle(dist, dist_target):
    Kp_theta = 0.01
    Kp_angle = 0.01

    error_theta = dist_target - dist

    theta_target = Kp_theta * error_theta
    theta = Lsensor.range

    error_angle = theta_target - theta

    start_angle = Kp_angle * error_angle
    start_angle = limit(start_angle, -0.3, 0.3)

    return start_angle, error_angle

# get correction and error terms for a target distance
error_line_integral, error_line_prev = 0, 0
def get_start_line(dist, dist_target):
    Kp, Ki, Kd = 0.01, 0.0005, 0.005

    global error_line_integral, error_line_prev
    error_line= dist_target - dist

    # update I
    error_line_integral += error_line
    error_line_integral = limit(error_line_integral, -100, 100) # windup

    # update D
    error_line_derivative = error_line- error_line_prev
    error_line_prev  = error_line

    start_line= Kp * error_line+ Ki * error_line_integral + Kd * error_line_derivative
    start_line= limit(start_line, -0.3, 0.3)
    return start_line, error_line

def run_control_loop(dist_target):
    dist, theta = get_odometry()
    start_angle, error_angle = get_start_angle(Lsensor.range, 90)
    start_line, error_line = get_start_line(dist, dist_target)
    right_motor.duty_cycle, left_motor.duty_cycle = int(abs((limit(start_line - start_angle, -1, 1))) * 65535), int(abs((limit(start_line + start_angle, -1, 1))) * 65535)
    return error_angle, error_line

def reset_odometry():
    left_enc.position, right_enc.position = 0, 0

def reset_controls():
    global error_angle_integral, error_angle_prev, error_line_integral, error_line_prev
    error_angle_integral, error_angle_prev, error_line_integral, error_line_prev = 0, 0, 0, 0

def forward():
    if Lsensor.range < 30:
        ledL.value = True
    else:
        ledL.value = False
        
    if Rsensor.range < 30:
        ledR.value = True
    else:
        ledR.value = False
    reset_odometry()
    while abs(run_control_loop(180)[1]) > 3:
        time.sleep(0.02)
    reset_controls()
    right_motor.duty_cycle, left_motor.duty_cycle = 0, 0

if __name__ == "__main__":
    while True:
        forward()
        time.sleep(1)
