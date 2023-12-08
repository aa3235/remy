import board
import busio
import time
import analogio
import pwmio
import digitalio
import rotaryio

#time.sleep(10)

motor2 = pwmio.PWMOut(board.GP2, frequency = 1000)

d1 = digitalio.DigitalInOut(board.GP1)
d1.direction = digitalio.Direction.OUTPUT
d2 = digitalio.DigitalInOut(board.GP0)
d2.direction = digitalio.Direction.OUTPUT

motor1 = pwmio.PWMOut(board.GP5, frequency = 1000)

d3 = digitalio.DigitalInOut(board.GP4)
d3.direction = digitalio.Direction.OUTPUT
d4 = digitalio.DigitalInOut(board.GP3)
d4.direction = digitalio.Direction.OUTPUT

d1.value = 0 #backwards left
d2.value = 1 #forwards

d3.value = 1 #backwards right
d4.value = 0 #forwards

left_enc = rotaryio.IncrementalEncoder(board.GP21, board.GP20)  #first one is a second is b
left_last_position = None
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)  #first one is a second is b
right_last_position = None
left_enc.position = 0
right_enc.position = 0

while True:
    d1.value = 0 #backwards left
    d2.value = 1 #forwards

    d3.value = 1 #backwards right
    d4.value = 0 #forwards
    
    
    
    left_position = left_enc.position
    right_position = right_enc.position
    print("1")
    if left_last_position == None or left_position != left_last_position:
        print("left pos = ", left_position)
        print("2")
    left_last_position = left_position
    if right_last_position == None or right_position != right_last_position:
        print("right pos = ", right_position)
        print("3")
    right_last_position = right_position

    if left_position > -90:
        motor1.duty_cycle = 35000
        print("4")
    else:
        motor1.duty_cycle = 0
    if right_position < 90:
        motor2.duty_cycle = 35000
        print("5")
    else:
        motor2.duty_cycle = 0
        print("6")

    
    

