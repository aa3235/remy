import rotaryio
import time
import board
import busio
import analogio
import pwmio
import digitalio
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