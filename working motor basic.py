from board import digitalio , PWM
from utime import sleep

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

def RotateCW(duty):
    ina1.value(1)
    ina2.value(0)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def RotateCCW(duty):
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

    
def RotateLeft(duty):
    ina1.value(0)
    ina2.value(1)
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

def RotateRight(duty):
    ina1.value(1)
    ina2.value(0)
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty*65536)/100)
    pwma.duty_u16(duty_16)
    pwmb.duty_u16(duty_16)

while True:
    duty_cycle=float(input("Enter pwm duty cycle"))
    print (duty_cycle)
    RotateCW(duty_cycle)
    sleep(2)
    RotateCCW(duty_cycle)
    sleep(2)
    RotateLeft(duty_cycle)
    sleep(1)
    RotateRight(duty_cycle)
    sleep(1)
    StopMotor()