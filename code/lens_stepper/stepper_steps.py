def step_1(self):
  self.GPIO.output(self.IN4, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN4, False)

def step_2(self):
  self.GPIO.output(self.IN4, True)
  self.GPIO.output(self.IN3, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN4, False)
  self.GPIO.output(self.IN3, False)

def step_3(self):
  self.GPIO.output(self.IN3, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN3, False)

def step_4(self):
  self.GPIO.output(self.IN2, True)
  self.GPIO.output(self.IN3, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN2, False)
  self.GPIO.output(self.IN3, False)

def step_5(self):
  self.GPIO.output(self.IN2, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN2, False)

def step_6(self):
  self.GPIO.output(self.IN1, True)
  self.GPIO.output(self.IN2, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN1, False)
  self.GPIO.output(self.IN2, False)

def step_7(self):
  self.GPIO.output(self.IN1, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN1, False)

def step_8(self):
  self.GPIO.output(self.IN4, True)
  self.GPIO.output(self.IN1, True)
  self.sleep(self.step_wait_time)
  self.GPIO.output(self.IN4, False)
  self.GPIO.output(self.IN1, False)

def stepper_clockwise(self, steps):
  for i in range(steps):
    if (self.stop_moving == True):
      return False

    # print("c " + str(i))
    step_8(self) # could put these in an array, call them that way, reverse
    step_7(self)
    step_6(self)
    step_5(self)
    step_4(self)
    step_3(self)
    step_2(self)
    step_1(self)

  return True

def stepper_counter_clockwise(self, steps):
  for i in range(steps):
    if (self.stop_moving == True):
      return False

    # print("cc " + str(i))
    step_1(self)
    step_2(self)
    step_3(self)
    step_4(self)
    step_5(self)
    step_6(self)
    step_7(self)
    step_8(self)
  
  return True
  