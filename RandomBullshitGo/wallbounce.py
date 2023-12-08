import board
import time
from math import pi
import digitalio
import rotaryio
import pwmio
import busio
import adafruit_tca9548a
import adafruit_vl6180x

print("start")
#time.sleep(20)

#LED
ledL = digitalio.DigitalInOut(board.GP18)
ledL.direction = digitalio.Direction.OUTPUT
ledR = digitalio.DigitalInOut(board.GP19)
ledR.direction = digitalio.Direction.OUTPUT

#Sensors
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA
mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Rsensor = adafruit_vl6180x.VL6180X(mux[5])
Fsensor = adafruit_vl6180x.VL6180X(mux[7])
Lsensor = adafruit_vl6180x.VL6180X(mux[6])


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

def limit(val):
    return min(1, max(val, -1))

if __name__ == "__main__":
    mm_per_tick = pi * Wheel_Diameter / Ticks_Per_Turn #gets distance travelled per tick of encoder
    
    right_dist  = right_enc.position * mm_per_tick
    left_dist = left_enc.position * mm_per_tick

    dist  = (right_dist + left_dist) / 2
    theta = (left_dist - right_dist) / Dist_Betwix_Wheels
    
    
    # angular P control
    Kp_angle = 0.9
    theta_target = 0

    error_angle = theta_target - theta
    start_angle = Kp_angle * error_angle
    
    # Linear P control
    Kp_line = 0.1
    dist_target = 20002

    error_line = dist_target - dist
    start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast

    while True:
        if Lsensor.range < 30:
            ledL.value = True
        else:
            ledL.value = False
            
        if Rsensor.range < 30:
            ledR.value = True
        else:
            ledR.value = False
        while error_line > 0:
            right_dist  = right_enc.position * mm_per_tick
            left_dist = left_enc.position * mm_per_tick

            dist  = (right_dist + left_dist) / 2
            theta = (left_dist - right_dist) / Dist_Betwix_Wheels
            
            
            # angular P control
            Kp_angle = 0.9
            theta_target = 0

            error_angle = theta_target - theta
            start_angle = Kp_angle * error_angle
            
            # Linear P control
            Kp_line = 0.1
            dist_target = 20000

            error_line = dist_target - dist
            start_line = limit(Kp_line * error_line) # 0.9 is a bit too fast
            

            # combine

            print(error_angle, error_line)
            
            
            right_motor.duty_cycle, left_motor.duty_cycle = int(abs((limit(start_line - start_angle))) * 30000), int(abs((limit(start_line + start_angle))) * 30000)
            
            print('R Range: {0}mm'.format(Rsensor.range))
            print('F Range: {0}mm'.format(Fsensor.range))
            print('L Range: {0}mm'.format(Lsensor.range))
            
            if Lsensor.range < 30:
                left_motor.duty_cycle = left_motor.duty_cycle + 500
                right_motor.duty_cycle = right_motor.duty_cycle - 500
            elif Lsensor.range > 70:
                left_motor.duty_cycle = left_motor.duty_cycle - 500
                right_motor.duty_cycle = right_motor.duty_cycle + 500

            #time.sleep(0.000005)
            
        right_motor.duty_cycle, left_motor.duty_cycle = 0, 0


