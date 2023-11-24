import board
import pwmio
import digitalio

#Define pmw and directions for the left motor
motor_left_pwm = pwmio.PWMOut(board.GP2, frequency = 1000)
motor_left_dir1 = digitalio.DigitalInOut(board.GP0)
motor_left_dir1.direction = digitalio.Direction.OUTPUT
motor_left_dir2 = digitalio.DigitalInOut(board.GP1)
motor_left_dir2.direction = digitalio.Direction.OUTPUT

#Define pmw and directions for the right motor
motor_right_pwm = pwmio.PWMOut(board.GP5, frequency = 1000)
motor_right_dir1 = digitalio.DigitalInOut(board.GP3)
motor_right_dir1.direction = digitalio.Direction.OUTPUT
motor_right_dir2 = digitalio.DigitalInOut(board.GP4)
motor_right_dir2.direction = digitalio.Direction.OUTPUT


#Function to control speed of left motor
def motor_left_speed(speed):
    if speed > 0:
        motor_left_dir1.value = True
        motor_left_dir2.value = False
    elif speed < 0:
        motor_left_dir1.value = False
        motor_left_dir2.value = True
    else:
        motor_left_dir1.value = False
        motor_left_dir2.value = False
    motor_left_pwm.duty_cycle = int(abs(speed) * 65535)

#Function to control speed of right motor
def motor_right_speed(speed):
    if speed > 0:
        motor_right_dir1.value = True
        motor_right_dir2.value = False
    elif speed < 0:
        motor_right_dir1.value = False
        motor_right_dir2.value = True
    else:
        motor_right_dir1.value = False
        motor_right_dir2.value = False
        
    motor_right_pwm.duty_cycle = int(abs(speed) * 65535) #make speed a positive integer and then * max pmw to use 0 - 1 as speed values instead of thousands
    
    
#Function to control both motors together
def speed(speed_left_wheel, speed_right_wheel):
    motor_left_speed(speed_left_wheel)
    motor_right_speed(speed_right_wheel)

#Function to make both motors go forward
def forward(speed):
    if speed > 0:
        motor_left_dir1.value = True
        motor_left_dir2.value = False
        motor_right_dir1.value = True
        motor_right_dir2.value = False
        motor_left_pwm.duty_cycle = int(abs(speed) * 65535)
        motor_right_pwm.duty_cycle = int(abs(speed) * 65535)

#Function to make both motors go backwards
def backward(speed):
    if speed > 0:
        motor_left_dir1.value = False
        motor_left_dir2.value = True
        motor_right_dir1.value = False
        motor_right_dir2.value = True
        motor_left_pwm.duty_cycle = int(abs(speed) * 65535)
        motor_right_pwm.duty_cycle = int(abs(speed) * 65535)

#Function to make both motors stop
def stop():
    motor_left_dir1.value = False
    motor_left_dir2.value = False
    motor_right_dir1.value = False
    motor_right_dir2.value = False