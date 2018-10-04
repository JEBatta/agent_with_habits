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

myfile = open("influence_single_node.csv","w")
myfile.write("x,y,motor1,motor2,V,A\n")

for x in np.arange(0.35,0.65,0.01):
 for y in np.arange(0.35,0.65,0.01):
  a = SensorimotorState([],[x,y])
  mu = m.influence(a)
  w = str(x)+","+str(y)+","+str(mu[0])+","+str(mu[1])+","+str(m.V(a))+","+str(m.A(a))+"\n"
  myfile.write(w)

myfile.close()

