import board
import busio
import adafruit_tca9548a
import adafruit_vl6180x
from machine import Pin , PWM
from utime import sleep
## sensor code
i2c0 = busio.I2C(board.GP1, board.GP0) // Left sensor
i2c1 = busio.I2C(board.GP11, board.GP10) // front sensor

Fsensor = adafruit_vl6180x.VL6180X(i2c1)

print('F Range: {0}mm'.format(Fsensor.range))


##motor code
led = Pin(25,Pin.OUT)
ina1 = Pin(18,Pin.OUT)
ina2 = Pin(17, Pin.OUT)
inb1 = Pin(13,Pin.OUT)
inb2 = Pin(14, Pin.OUT)

pwma = PWM(Pin(16))
pwmb = PWM(Pin(15))

pwma.freq(1000)
pwmb.freq(1000)

led.toggle()

# PWM for Motor 

def RotateCW(duty):  #forwards
    ina1.value(1)
    ina2.value(0)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)
    DistForward = Fsensor.range

def RotateCCW(duty): # backwards
    ina1.value(0)
    ina2.value(1)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)
    
def StopMotor():
    ina1.value(0)
    ina2.value(0)
    inb1.value(0)
    inb2.value(0)
    pwma.duty_u16(0)
    pwmb.duty_u16(0)

    
def RotateLeft(duty): #turn left
    ina1.value(0)
    ina2.value(1)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def RotateRight(duty): #turn right
    ina1.value(1)
    ina2.value(0)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)


While True:
    try RotateCW(30)
    except Fsensor.range > 15:
       
    
