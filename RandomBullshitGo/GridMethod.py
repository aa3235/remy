import board
import busio
import time
import analogio
import pwmio
import digitalio
import rotaryio

motor1 = pwmio.PWMOut(board.GP2, frequency = 1000)
motor2 = pwmio.PWMOut(board.GP5, frequency = 1000)
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)  #first one is a second is b
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)  #first one is a second is b



d1 = digitalio.DigitalInOut(board.GP1)
d1.direction = digitalio.Direction.OUTPUT
d2 = digitalio.DigitalInOut(board.GP0)
d2.direction = digitalio.Direction.OUTPUT

d3 = digitalio.DigitalInOut(board.GP4)
d3.direction = digitalio.Direction.OUTPUT
d4 = digitalio.DigitalInOut(board.GP3)
d4.direction = digitalio.Direction.OUTPUT

def forwards():
    left_enc.position = 0
    right_enc.position = 0

    d1.value = 0
    d2.value = 1

    d3.value = 0
    d4.value = 1

    motor1.duty_cycle = 60000
    motor2.duty_cycle = 60000

    running = False


    sec = 6000
    left_last_position = None
    right_last_position = None
    while sec > 0:
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
            #+print("1")
        if left_position < right_position:
            motor1.duty_cycle = 55000
            motor2.duty_cycle = 0
            #print("2")
        if left_position == right_position:
            motor1.duty_cycle = 55000
            motor2.duty_cycle = 55000
            #print("3")
        sec = sec -1
        #print("4")
        
        
        if sec == 0:
            motor1.duty_cycle = 0
            motor2.duty_cycle = 0
             
            print("done")
            time.sleep(3)
    #         sec = 6000
    
    
def right():
    left_last_position = None
    right_last_position = None
    
    d1.value = 0
    d2.value = 1

    d3.value = 1
    d4.value = 0


    while True:
        left_position = left_enc.position
        right_position = right_enc.position
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
        left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
        right_last_position = right_position
        
        if left_position < 33:
            motor1.duty_cycle = 45000
        else:
            motor1.duty_cycle = 0
        if right_position > -33:
            motor2.duty_cycle = 45000
        else:
            motor2.duty_cycle = 0
            
        print("5")
        time.sleep(3)
        
            

def left():
    left_last_position = None
    right_last_position = None
    while True:
        d1.value = 1 #backwards left
        d2.value = 0 #forwards

        d3.value = 0 #backwards right
        d4.value = 1 #forwards
        
        
        
        left_position = left_enc.position
        right_position = right_enc.position
        if left_last_position == None or left_position != left_last_position:
            print("left pos = ", left_position)
        left_last_position = left_position
        if right_last_position == None or right_position != right_last_position:
            print("right pos = ", right_position)
        right_last_position = right_position

        if left_position > -37:
            motor1.duty_cycle = 45000
        else:
            motor1.duty_cycle = 0
        if right_position < 37:
            motor2.duty_cycle = 45000
        else:
            motor2.duty_cycle = 0
            
            
        print("6")
        time.sleep(3)

while True:
    forwards()
    print("7")
    forwards()
    print("8")
    left_enc.position = 0
    right_enc.position = 0
    left()
    print("9")
    left_enc.position = 0
    right_enc.position = 0
    forwards()
    print("10")
    left_enc.position = 0
    right_enc.position = 0
    right()
    print("11")
    left_enc.position = 0
    right_enc.position = 0


    


