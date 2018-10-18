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
myfile.write("x,y,motor1,motor2,V1,V2,A1,A2\n")

for m2 in np.arange(0.35,0.65,0.01):
 for m1 in np.arange(0.35,0.65,0.01):
  a = SensorimotorState([],[m1,m2])
  mu = m.influence(a)
  Va = m.V(a)
  Aa = m.A(a)
  w = str(m1)+","+str(m2)+","+str(mu[0])+","+str(mu[1])+","+str(Va[0])+","+str(Va[1])+","+str(Aa[0])+","+str(Aa[1])+"\n"
  myfile.write(w)

myfile.close()

