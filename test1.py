from agent_system import SensorimotorState
from agent_system import Node
from agent_system import Medium
import numpy as np

#Infuence of a single node

sm = SensorimotorState([],[0.5,0.5])
v = [0,0.1]

m = Medium()
m.addNode(sm,v)
for n in m.nodes:
 n.timeBeforeActive = 0
 n.activation = True

for x in np.arange(0.35,0.65,0.01):
 for y in np.arange(0.35,0.65,0.01):
  a = SensorimotorState([],[x,y])
  mu = m.influence(a)
  print(x,y,mu[0],mu[1])

