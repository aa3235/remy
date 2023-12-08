import board
import busio
import time
import analogio
import pwmio
import digitalio
import rotaryio



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

left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)  #first one is a second is b
left_last_position = None
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)  #first one is a second is b
right_last_position = None


while True:
    left_position = left_enc.position
    right_position = right_enc.position
    if left_last_position == None or left_position != left_last_position:
        print("left pos = ", left_position)
    left_last_position = left_position
    if right_last_position == None or right_position != right_last_position:
        print("right pos = ", right_position)
    right_last_position = right_position
    
    motor1.duty_cycle = 55000
    motor2.duty_cycle = 55000
    
    if left_position > right_position:
        motor1.duty_cycle = 0
        motor2.duty_cycle = 55000
    if left_position < right_position:
        motor1.duty_cycle = 55000
        motor2.duty_cycle = 0
    if left_position == right_position:
        motor1.duty_cycle = 55000
        motor2.duty_cycle = 55000
        


    

