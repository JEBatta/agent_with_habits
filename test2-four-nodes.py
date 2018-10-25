from agent_system import SensorimotorState
from agent_system import Node
from agent_system import Medium
import numpy as np

#Infuence of four nodes

s1 = SensorimotorState([],[0.45,0.5])
s2 = SensorimotorState([],[0.5,0.55])
s3 = SensorimotorState([],[0.55,0.5])
s4 = SensorimotorState([],[0.5,0.45])
v1 = [0,1]
v2 = [1,0]
v3 = [0,-1]
v4 = [-1,0]

weight = 100.0 #Use the values -500, -100, 0, 50 and 100 
m = Medium()
m.addNode(s1,v1)
m.addNode(s2,v2)
m.addNode(s3,v3,weight)
m.addNode(s4,v4)

for n in m.nodes:
 n.timeBeforeActive = 0
 n.activation = True

myfile = open("influence_four_nodes.csv","w")
myfile.write("w,x,y,motor1,motor2\n")

for m2 in np.arange(0.35,0.65,0.01):
 for m1 in np.arange(0.35,0.65,0.01):
  a = SensorimotorState([],[m1,m2])
  mu = m.influence(a)
  w = str(weight)+","+str(m1)+","+str(m2)+","+str(mu[0])+","+str(mu[1])+"\n"
  myfile.write(w)

myfile.close()
