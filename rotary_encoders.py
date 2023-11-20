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
    pos_left = left_enc.position
    pos_right = right_enc.position
    if last_pos_left == None or pos_left != last_pos_left:
        print("left pos = ", pos_left)
    left_last_position = left_position
    if last_pos_right == None or pos_right != last_pos_right:
        print("right pos = ", pos_right)
    last_pos_right = pos_right
