
class Robot:
 
 def __init__(self,x):
  self.x = x
  self.m = 0
  self.s = 0

 def SensorUpdate(self, light):
  self.s = 1 / (1 + (self.x - light.x)**2)

 def MotorAction(self,dt = 1):
  self.x = self.x + dt * self.m

 def SetPosition(self, x0):
  self.x = x0
 
 def MotorUpdate(self,newm):
  newm = max(min(newm,1),-1)
  self.m = newm

class Light:

 def __init__(self,x = 0):
  self.x = x



