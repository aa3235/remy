import board
import busio
import time
import analogio
import pwmio
import digitalio
import rotaryio
import adafruit_tca9548a
import adafruit_vl6180x

#encoder definitions
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)  #first one is a second is b
left_last_position = None
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)  #first one is a second is b
right_last_position = None
left_position = left_enc.position
right_position = right_enc.position

#motors

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

motor1.duty_cycle = 60000
motor2.duty_cycle = 60000

running = False


#sensor time
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA

mux = adafruit_tca9548a.TCA9548A(i2c) # make tsa (multiplexer) object using i2c

Fsensor = adafruit_vl6180x.VL6180X(mux[0])


#functions

def left():
    left_done= False
    right_done = False
    
    while left_done == False and right_done == False:
    
        d1.value = 1 #backwards left
        d2.value = 0 #forwards

        d3.value = 0 #backwards right
        d4.value = 1 #forwards
        
        left_position = left_enc.position
        right_position = right_enc.position
        
        left_last_position = None
        right_last_position = None
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
        left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
        right_last_position = right_position
        
        if left_position > -44:
            motor1.duty_cycle = 45000
        else:
            motor1.duty_cycle = 0
            left_done = True
        if right_position < 44:
            motor2.duty_cycle = 45000
        else:
            motor2.duty_cycle = 0
            right_done = True

    d1.value = 0
    d2.value = 1

    d3.value = 0
    d4.value = 1





while True:
    if Fsensor.range < 70:
        motor1.duty_cycle = 0
        motor2.duty_cycle = 0
        time.sleep(2)
        print("left")
        left_enc.position = 0
        right_enc.position = 0
        left()
        left_enc.position = 0
        right_enc.position = 0
    else:
        left_position = left_enc.position
        right_position = right_enc.position
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
        left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
        right_last_position = right_position
        
        if left_position > right_position:
            motor1.duty_cycle = 0
            motor2.duty_cycle = 55000
        if left_position < right_position:
            motor1.duty_cycle = 55000
            motor2.duty_cycle = 0
        if left_position == right_position:
            motor1.duty_cycle = 55000
            motor2.duty_cycle = 55000

