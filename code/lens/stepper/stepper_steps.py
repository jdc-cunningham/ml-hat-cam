def step_1(self):
    GPIO.output(self.IN4, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN4, False)

def step_2(self):
    GPIO.output(self.IN4, True)
    GPIO.output(self.IN3, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN4, False)
    GPIO.output(self.IN3, False)

def step_3(self):
    GPIO.output(self.IN3, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN3, False)

def step_4(self):
    GPIO.output(self.IN2, True)
    GPIO.output(self.IN3, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN2, False)
    GPIO.output(self.IN3, False)

def step_5(self):
    GPIO.output(self.IN2, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN2, False)

def step_6(self):
    GPIO.output(self.IN1, True)
    GPIO.output(self.IN2, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN1, False)
    GPIO.output(self.IN2, False)

def step_7(self):
    GPIO.output(self.IN1, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN1, False)

def step_8(self):
    GPIO.output(self.IN4, True)
    GPIO.output(self.IN1, True)
    sleep (self.step_wait_time)
    GPIO.output(self.IN4, False)
    GPIO.output(self.IN1, False)

def stepper_clockwise(self, steps):
  for i in range(steps):
    if (self.stop_moving == True):
      return False

    # print("c " + str(i))
    step_8() # could put these in an array, call them that way, reverse
    step_7()
    step_6()
    step_5()
    step_4()
    step_3()
    step_2()
    step_1()

  return True

def stepper_counter_clockwise(self, steps):
  for i in range(steps):
    if (self.stop_moving == True):
      return False

    # print("cc " + str(i))
    step_1()
    step_2()
    step_3()
    step_4()
    step_5()
    step_6()
    step_7()
    step_8()
  
  return True
  