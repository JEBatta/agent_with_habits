import numpy as np
import math

class SensorimotorState:
 
 def __init__(self,s,m):
  self.sensorDim = len(s)
  self.motorDim = len(m)
  self.state =np.concatenate((np.array(s),np.array(m)),axis = 0)

 def distanceFactor(self,state,kd=1000.0):
  try:
   d = math.exp(kd*(np.linalg.norm(self.state-np.array(state)))**2)
   return float(2/(1+d))
  except OverflowError:
   return 0

class Node:
 
 def __init__(self,smstate,velocity,weight = 0.0,tba=10.0):
  if isinstance(smstate,SensorimotorState):
   self.smstate = smstate
  else:
   self.smstate = None
  self.velocity = np.array(velocity)
  self.weight = weight
  self.activation = False
  self.timeBeforeActive = tba
 
 def distanceFactor(self, point,kd=1000.0):
  if isinstance(point,SensorimotorState):
   return self.smstate.distanceFactor(point.state,kd)
 
 def weightFactor(self,kw = 0.0025):
  try:
   return 2 / (1 + math.exp(-kw*self.weight))
  except OverflowError:
   return 0

 def updateNode(self,smstate,krej = 10.0,kdeg = 1.0,dt = 0.01):
  if isinstance(smstate,SensorimotorState):
   self.weight += dt*(- kdeg + krej * self.distanceFactor(smstate))
   if self.timeBeforeActive > 0:
    self.timeBeforeActive -= dt
   if self.timeBeforeActive <= 0:
    self.activation = True  

 def Gamma(self,smstate):
  NvNorm = np.linalg.norm(self.velocity)
  if NvNorm == 0:
   return smstate.state
  normState = self.velocity/NvNorm
  return smstate.state - np.dot(smstate.state,normState) * normState

  
class Medium:
 def __init__(self):
  self.nodes = []

 def density(self,smstate,kd = 1000,kw = 0.0025,onlyActivatedNodes = False):
  if not isinstance(smstate,SensorimotorState):
   return None
  d = 0
  if onlyActivatedNodes:
   nodeSet = [nd for nd in self.nodes if nd.activation]
  else:
   nodeSet = self.nodes 
  for n in nodeSet:
   d += n.weightFactor(kw) * n.distanceFactor(smstate,kd)
  return d

 def addNode(self,smstate,velocity,weight=1.0,kt = 1, tba = 10.0):
  if isinstance(smstate,SensorimotorState) and self.density(smstate) < kt:
   self.nodes.append(Node(smstate,velocity,weight,tba))

 def updateNodes(self,smstate,krej = 10.0,kdeg = 1.0,dt = 0.01):
  if isinstance(smstate,SensorimotorState):
   for n in self.nodes:
    n.updateNode(smstate,krej,kdeg,dt)

 def V(self,smstate, kd = 1000,kw = 0.0025):
  v = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   npmotor = n.velocity[n.smstate.sensorDim:]
   v+= n.weightFactor(kw) * n.distanceFactor(smstate,kd) * npmotor 
  return np.array(v)

 def A(self,smstate, kd = 1000,kw = 0.0025):
  a = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   dum1 = n.smstate.state - smstate.state
   dum2 = SensorimotorState(dum1[:smstate.sensorDim],dum1[smstate.sensorDim:])
   Gmotor = n.Gamma(dum2)
   Gmotor = Gmotor[n.smstate.sensorDim:]
   a+= n.weightFactor(kw) * n.distanceFactor(smstate,kd) * Gmotor
  return np.array(a)

 def influence(self,smstate,kd = 1000,kw = 0.0025):
  V = self.V(smstate,kd,kw)
  A = self.A(smstate,kd,kw)
  dmu = np.array([0]*smstate.motorDim)
  if np.linalg.norm(V+A) > 0:
   dmu = (A + V) / self.density(smstate,kd,kw,True)
  return dmu
