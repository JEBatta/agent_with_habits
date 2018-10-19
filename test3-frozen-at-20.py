from agent_system import SensorimotorState
from agent_system import Node
from agent_system import Medium
import numpy as np
import math

# training a medium 20 time-units and then frozen its influence
m = Medium()
s0=SensorimotorState([],[0.875,0.5]) 
for t in range(1,21):
 m1 = (1 + 0.75*math.cos(2*math.pi*t/10))/ 2
 m2 = (1 + 0.75*math.sin(2*math.pi*t/10))/ 2
 s = SensorimotorState([],[m1,m2])
 v = s.state-s0.state
 m.addNode(s0,v)
 m.updateNodes(s0)
 s0 = s

for n in m.nodes:
 n.timeBeforeActive = 0
 n.activation = True

myfile = open("influence_frozen_at_20.csv","w")
myfile.write("m1,m2,dm1,dm2,v1,v2,a1,a2\n")

for y in np.arange(0.0,1.0,0.01):
 for x in np.arange(0.0,1.0,0.01):
  a = SensorimotorState([],[x,y])
  mu = m.influence(a)
  Va = m.V(a)
  Aa = m.A(a)
  w = str(x)+","+str(y)+","+str(mu[0])+","+str(mu[1])+","+str(Va[0])+","+str(Va[1])+","+str(Aa[0])+","+str(Aa[1])+"\n"
  myfile.write(w)

myfile.close()
