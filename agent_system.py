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
  self.velocity = np.array(velocity)
  self.weight = 0.0
  self.activation = False
  self.timeBeforeActive = 10
 
 def distanceFactor(self, point,kd=1000.0):
  if isinstance(point,Node):
   return self.smstate.distanceFactor(point.smstate.state,kd)
  if isinstance(point,SensorimotorState):
   return self.smstate.distanceFactor(point.state,kd)
  if isinstance(point,np.array):
   return self.smstate.distanceFactor(point,kd)
 
 def weightFactor(self,kw = 0.0025):
  return 2 / (1 + math.exp(-kw*self.weight))

 def updateNode(self,state):
  self.weight += -1.0 + 10.0 * self.distanceFactor(state)
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

 def density(self,smstate):
  if not isinstance(smstate,SensorimotorState):
   return None
  d = 0
  for n in [nd for nd in self.nodes if nd.activation]:
   d += n.weightFactor() * n.distanceFactor(smstate) 
  return d

 def addNode(self,smstate,velocity,kt = 1):
  if isinstance(smstate,SensorimotorState) and self.density(smstate) < kt:
   self.nodes.append(Node(smstate,velocity))
  else:
   print "addNode input is not a Node."

 def updateNodes(self,state):
  for n in self.nodes():
   n.updateNode(state)

 def V(self,smstate):
  v = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   npmotor = n.velocity[n.smstate.sensorDim:]
   v+= n.weightFactor() * n.distanceFactor(smstate) * npmotor 
  return v

 def A(self,smstate):
  a = [0]*smstate.motorDim
  for n in [nd for nd in self.nodes if nd.activation]:
   dum1 = n.smstate.state - smstate.state
   dum2 = SensorimotorState(dum1[:smstate.sensorDim],dum1[smstate.sensorDim:])
   Gmotor = n.Gamma(dum2)
   Gmotor = Gmotor[n.smstate.sensorDim:]
   a+= n.weightFactor() * n.distanceFactor(smstate) * Gmotor 
  return a

 def influence(self,smstate):
  return (self.V(smstate) + self.A(smstate)) / self.density(smstate)
