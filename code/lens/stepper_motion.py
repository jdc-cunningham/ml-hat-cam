# https://github.com/custom-build-robots/Stepper-motor-28BYJ-48-Raspberry-Pi/blob/master/decision-maker.py

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Stepper Pins
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26

# waiting time - speed motor turns
time = 0.001

def init_gpio_pins():
    # set GPIO pins
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)

    # set pins to false
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def step_1():
    GPIO.output(IN4, True)
    sleep (time)
    GPIO.output(IN4, False)

def step_2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)

def step_3():
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN3, False)

def step_4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep (time)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)

def step_5():
    GPIO.output(IN2, True)
    sleep (time)
    GPIO.output(IN2, False)

def step_6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep (time)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)

def step_7():
    GPIO.output(IN1, True)
    sleep (time)
    GPIO.output(IN1, False)

def step_8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep (time)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)

def stepper_clockwise(steps):
    for i in range(steps):
        step_8() # could put these in an array, call them that way, reverse
        step_7()
        step_6()
        step_5()
        step_4()
        step_3()
        step_2()
        step_1()

def stepper_counter_clockwise(steps):
    for i in range(steps):
        step_1()
        step_2()
        step_3()
        step_4()
        step_5()
        step_6()
        step_7()
        step_8()
