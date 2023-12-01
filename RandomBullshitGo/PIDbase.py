import board
import time
from math import pi
import digitalio
import rotaryio
import pwmio
import adafruit_motor.motor as motor

time.sleep(30)


Ticks_Per_Turn = 60
Dist_Betwix_Wheels = 116
Wheel_Diameter = 40.0 # mm


# encoders
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)

# motors
left_motor = pwmio.PWMOut(board.GP2, frequency = 1000)

left_motor_dir_1 = digitalio.DigitalInOut(board.GP1)
left_motor_dir_1.direction = digitalio.Direction.OUTPUT
left_motor_dir_2 = digitalio.DigitalInOut(board.GP0)
left_motor_dir_2.direction = digitalio.Direction.OUTPUT

right_motor = pwmio.PWMOut(board.GP5, frequency = 1000)

right_motor_dir_1 = digitalio.DigitalInOut(board.GP4)
right_motor_dir_1.direction = digitalio.Direction.OUTPUT
right_motor_dir_2 = digitalio.DigitalInOut(board.GP3)
right_motor_dir_2.direction = digitalio.Direction.OUTPUT

left_motor_dir_1.value = 0
left_motor_dir_2.value = 1

right_motor_dir_1.value = 0
right_motor_dir_2.value = 1


""" Main """

def limit(val):
    return min(1, max(val, -1))

if __name__ == "__main__":
    mm_per_tick = pi * Wheel_Diameter / Ticks_Per_Turn #gets distance travelled per tick of encoder
    
    left_dist  = left_enc.position * mm_per_tick
    right_dist = right_enc.position * mm_per_tick

    dist  = (left_dist + right_dist) / 2
    theta = (right_dist - left_dist) / Dist_Betwix_Wheels
    
    
    # angular P control
    Kp_angle = 0.9
    theta_target = 0

    error_angle = theta_target - theta
    start_angle = Kp_angle * error_angle
    
    # Linear P control
    Kp_line = 0.1
    dist_target = 110

    error_line = dist_target - dist
    start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast

    while True:
        while error_line > 0:
            left_dist  = left_enc.position * mm_per_tick
            right_dist = right_enc.position * mm_per_tick

            dist  = (left_dist + right_dist) / 2
            theta = (right_dist - left_dist) / Dist_Betwix_Wheels
            
            
            # angular P control
            Kp_angle = 0.9
            theta_target = 0

            error_angle = theta_target - theta
            start_angle = Kp_angle * error_angle
            
            # Linear P control
            Kp_line = 0.1
            dist_target = 110

            error_line = dist_target - dist
            start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast
            

            # combine

            print(error_angle, error_line)
            
            
            left_motor.duty_cycle, right_motor.duty_cycle = int(abs((limit(start_line - start_angle))) * 65535), int(abs((limit(start_line + start_angle))) * 65535)

            #time.sleep(0.000005)
            
        left_motor.duty_cycle, right_motor.duty_cycle = 0, 0
