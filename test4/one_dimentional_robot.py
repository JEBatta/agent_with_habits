
class Robot:
 
 def __init__(self,x,light):
  self.x = x
  self.m = 0
  self.s = 1 / (1 + (x - light.x)**2)
# In methods is assumed that
# sensor and motor imputs are already
# normalized. Outputs are normalized too.

 def SensorUpdate(self, light):
  self.s = 1 / (1 + (self.x - light.x)**2)

 def PositionUpdate(self,dt = 1, byForce = False, forcedx = 0.0):
  self.x = self.x - dt * self.m
  if byForce:
   self.x = forcedx
 
 def MotorUpdate(self,nm):
  #if nm > 1:
   #nm = 0.5
  #if nm < 0:
   #nm = 0.5
  self.m = (nm * 2) - 1

class Light:

 def __init__(self,x = 0):
  self.x = x



