import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
import time
import analogio
import pwmio
from math import pi
import digitalio
import rotaryio

time.sleep(20)

i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

#Rsensor = adafruit_vl6180x.VL6180X(mux[5])
Fsensor = adafruit_vl6180x.VL6180X(mux[7])
#Lsensor = adafruit_vl6180x.VL6180X(mux[6])

# encoders
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)
left_last_position = None
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)
right_last_position = None
left_position = left_enc.position
right_position = right_enc.position




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

def limit(val):
        return min(1, max(val, -1))
    
def forwards16():
    Ticks_Per_Turn = 60
    Dist_Betwix_Wheels = 116
    Wheel_Diameter = 40.0 # mm
    

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
        dist_target = 115

        error_line = dist_target - dist
        start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast

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
            dist_target = 115

            error_line = dist_target - dist
            start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast
            

            # combine

            print(error_angle, error_line)
            
            
            left_motor.duty_cycle, right_motor.duty_cycle = int(abs((limit(start_line - start_angle))) * 65535), int(abs((limit(start_line + start_angle))) * 65535)

            #time.sleep(0.000005)
            
        left_motor.duty_cycle, right_motor.duty_cycle = 0, 0
        
def left():
    global left_position
    global right_position
    global left_last_position
    global right_last_position
    
    left_enc.position = 0
    right_enc.position = 0
    left_done = False
    right_done = False

    while left_done == False or right_done == False:
        left_motor_dir_1.value = 1 #backwards left
        left_motor_dir_2.value = 0 #forwards

        right_motor_dir_1.value = 0 #backwards right
        right_motor_dir_2.value = 1 #forwards
        
        
        
        left_position = left_enc.position
        right_position = right_enc.position
        print("1")
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
            left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
            right_last_position = right_position
            print("2")

        if left_position > -37:
            left_motor.duty_cycle = 35000
            print("3")
        else:
            left_motor.duty_cycle = 0
            print("4")
            left_done = True
        if right_position < 37:
            right_motor.duty_cycle = 35000
            print("5")
        else:
            right_motor.duty_cycle = 0
            print("6")
            right_done = True
            

def right():
    global left_position
    global right_position
    global left_last_position
    global right_last_position
    left_enc.position = 0
    right_enc.position = 0
    left_done = False
    right_done = False
    while left_done == False or right_done == False:
        left_motor_dir_1.value = 0 #backwards left
        left_motor_dir_2.value = 1 #forwards

        right_motor_dir_1.value = 1 #backwards right
        right_motor_dir_2.value = 0 #forwards
    
        left_position = left_enc.position
        right_position = right_enc.position
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
        left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
        right_last_position = right_position
        
        if left_position < 37:
            left_motor.duty_cycle = 40000
        else:
            left_motor.duty_cycle = 0
            left_done = True
        if right_position > -37:
            right_motor.duty_cycle = 40000
        else:
            right_motor.duty_cycle = 0
            right_done = True
            

        

forwards16()
time.sleep(3)
left()
time.sleep(3)
right()