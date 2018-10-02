import numpy as np
import math

class SensorimotorState:
 
 def __init__(self,s,m):
  self.sensorDim = len(s)
  self.motorDim = len(m)
  self.state =np.concatenate((np.array(s),np.array(m)),axis = 0)

 def distance(self,state,kd=1000.0):
  try:
   d = math.exp(kd*np.linalg.norm(self.state-np.array(state))**2)
   return 2/(1+d)
  except ValueError:
   print "Sensorimotor states must have the same length."
  except OverflowError:
   return 0


class Node:
 
 def __init__(self,smstate,velocity):
  if isinstance(smstate,SensorimotorState):
   self.smstate = smstate
  else:
   self.smstate = None
  self.velocity = velocity
  self.weight = 0.0
 
 def distance(self, point,kd=1000.0):
  if isinstance(point,Node):
   return self.smstate.distance(point.smstate.state,kd)
  if isinstance(point,SensorimotorState):
   return self.smstate.distance(point.state,kd)
 
 def sigmoidalWeight(self,kw = 0.0025):
  return 2 / (1 + math.exp(-kw*self.weight))

 def updateWeight(self,state):
  self.weight += -1.0 + 10.0 * self.distance(state) 


class Medium:
 def __init__(self):
  self.nodes = []

 def addNode(self,node):
  if isinstance(node,Node):
   self.nodes.append(node)
  else:
   print "addNode input is not a Node."

