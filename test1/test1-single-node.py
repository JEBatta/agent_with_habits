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
  d = a.distanceFactor(sm.state)
  mu = m.influence(a,1000,0.0025)
  #Va = m.V(a)
  #Aa = m.A(a)
  w = str(m1)+","+str(m2)+","+str(mu[0])+","+str(mu[1])+","+str(d)+"\n"
  myfile.write(w)

myfile.close()

