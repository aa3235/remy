import rotary_encoders


# PID control parameters
kp = 0.05  # Proportional gain (adjust as needed)
ki = 0.002  # Integral gain (adjust as needed)
kd = 0.001  # Derivative gain (adjust as needed)

# Initialize variables for PID control for both motors
error_integral_left = 0
error_integral_right = 0
last_error_left = 0
last_error_right = 0
setpoint = 0.7  # Target RPS

# Initialize motors
motor_left = pwmio.PWMOut(board.GP2, frequency = 1000)

d1 = digitalio.DigitalInOut(board.GP1)
d1.direction = digitalio.Direction.OUTPUT
d2 = digitalio.DigitalInOut(board.GP0)
d2.direction = digitalio.Direction.OUTPUT  


motor_right = pwmio.PWMOut(board.GP5, frequency = 1000)

d3 = digitalio.DigitalInOut(board.GP4)
d3.direction = digitalio.Direction.OUTPUT
d4 = digitalio.DigitalInOut(board.GP3)
d4.direction = digitalio.Direction.OUTPUT 


#encoders
left_enc = rotaryio.IncrementalEncoder(board.GP6, board.GP7)  #first one is a second is b
left_last_position = None
right_enc = rotaryio.IncrementalEncoder(board.GP26, board.GP27)  #first one is a second is b
right_last_position = None

last_time = time.monotonic()

#get rpm from encoders
def get_rpm(pos, time_interval):
    if time_interval > 0:
        rpm = (pos / 60) / time_interval
        return rpm
    else:
        return 0
    
def PID_control():
    global motor_left, motor_right, error_integral_left, error_integral_right, last_error_left, last_error_right, setpoint, last_time
    current_time = time.monotonic()
    time_interval = current_time - last_time
    
    pos_left = left_enc.position
    pos_right = right_enc.position
    
    if time_interval > 0:
        rpm_left = calculate_rpm(pos_left, time_interval)
        rpm_right = calculate_rpm(pos_right, time_interval)

        print("left RPM = ", rpm_left)
        print("right RPM = ", rpm_right)
        
        #P
        error_left = rpm_right - rpm_left
        error_right = setpoint - rpm_right
        
        #I
        error_I_left = error_I_left + error_left * time_interval
        error_I_right = error_I_right + error_right * time_interval
        
        #D
        error_D_left = (error_left - previous_error_left) / time_interval
        error_D_right = (error_right - previous_error_right) / time_interval
        
        
        #Apply PID
        change_left = kp * error_left + ki * error_I_left + kd * error_D_left
        change_right = kp * error_right + ki * error_I_right + kd * error_D_right
        
        #Rewrite the motors so the change can be applied easier. (not sure if this works, if so maybe leave it)
        motor_left.duty_cycle = motor_left.duty_cycle + (changeleft * 65535)
        motor_right.duty_cycle = motor_right.duty_cycle + (changeright * 65535)
        
        last_time = current_time
        last_error_left = error_left
        last_error_right = error_right
        
        #reset encoders
        left_enc.position = 0
        right_enc.position = 0
        
    time.sleep(0.2)