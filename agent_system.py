import numpy as np
import math

class SensorimotorState:
 
 def __init__(self,s,m):
  self.sensorDim = len(s)
  self.motorDim = len(m)
  self.state =np.concatenate((np.array(s),np.array(m)),axis = 0)

 def distanceFactor(self,state,kd=1000.0):
  try:
   d = math.exp(kd*np.linalg.norm(self.state-np.array(state))**2)
   return float(2/(1+d))
  except ValueError:
   print "Sensorimotor states must have the same length."
  except OverflowError:
   return 0


class Node:
 
 def __init__(self,smstate,velocity,weight = 0.0):
  if isinstance(smstate,SensorimotorState):
   self.smstate = smstate
  else:
   self.smstate = None
  self.velocity = np.array(velocity)
  self.weight = weight
  self.activation = False
  self.timeBeforeActive = 10
 
 def distanceFactor(self, point,kd=1000.0):
  if isinstance(point,Node):
   return self.smstate.distanceFactor(point.smstate.state,kd)
  if isinstance(point,SensorimotorState):
   return self.smstate.distanceFactor(point.state,kd)
 
 def weightFactor(self,kw = 0.0025):
  return 2 / (1 + math.exp(-kw*self.weight))

 def updateNode(self,smstate,dt = 1):
  if isinstance(smstate,SensorimotorState):
   self.weight += dt*(- 1 + 10.0 * self.distanceFactor(smstate))
   if self.timeBeforeActive > 0:
    self.timeBeforeActive -= 1
   if self.timeBeforeActive == 0:
    self.activation = True 

 def Gamma(self,smstate):
  if np.linalg.norm(self.velocity) > 0:
   normState = self.velocity/np.linalg.norm(self.velocity)
   return smstate.state - np.dot(smstate.state,normState) * normState
  else:
   return smstate.state
   

class Medium:
 def __init__(self):
  self.nodes = []

 def density(self,smstate,kd = 1000,kw = 0.0025):
  if not isinstance(smstate,SensorimotorState):
   return None
  d = 0
  for n in [nd for nd in self.nodes if nd.activation]:
   d += n.weightFactor(kw) * n.distanceFactor(smstate,kd) 
  return d

 def addNode(self,smstate,velocity,weight=0.0,kt = 1):
  if isinstance(smstate,SensorimotorState) and self.density(smstate) < kt:
   self.nodes.append(Node(smstate,velocity,weight))

 def updateNodes(self,smstate,dt = 1):
  if isinstance(smstate,SensorimotorState):
   for n in self.nodes:
    n.updateNode(smstate,dt)

 def V(self,smstate, kd = 1000,kw = 0.0025):
  v = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   npmotor = n.velocity[n.smstate.sensorDim:]
   v+= (n.weightFactor(kw) * n.distanceFactor(smstate,kd) * npmotor) 
  return np.array(v)

 def A(self,smstate, kd = 1000,kw = 0.0025):
  a = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   dum1 = n.smstate.state - smstate.state
   dum2 = SensorimotorState(dum1[:smstate.sensorDim],dum1[smstate.sensorDim:])
   Gmotor = n.Gamma(dum2)
   Gmotor = Gmotor[n.smstate.sensorDim:]
   a+= (n.weightFactor(kw) * n.distanceFactor(smstate,kd) * Gmotor) 
  return np.array(a)

 def influence(self,smstate,kd = 1000,kw = 0.0025):
  try:
   dmu = (self.V(smstate,kd,kw) + self.A(smstate,kd,kw)) / self.density(smstate,kd,kw)
  except ZeroDivisionError: 
   dmu = np.array([float("Inf"),float("Inf")])
  return dmu
