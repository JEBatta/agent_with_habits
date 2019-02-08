from agent_system import SensorimotorState
from agent_system import Node
from agent_system import Medium
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

from one_dimentional_robot import Robot
from one_dimentional_robot import Light

light = Light(0)
robot = Robot(-2.5,light)
#robot.SensorUpdate(light)
medium = Medium()
m0 = (robot.m + 1)/ 2
s0 = robot.s
sm = SensorimotorState([s0],[m0])

dt = 0.05
kd = 1000
kw = 0.0025
krej = 10.0
kdeg = 1.0	
kt = 1.0
tba = 10.0
ttrain = 20
tpert = 35
tcontrol = 200
################
ampFactor = 3.0 
################
# This factor was introduced to increase
# the influence of medium in robot movement
################
time = []
position = []
sensor = []
motor = []
### training stage

tfile = open("test4_record_on_time","w")
tfile.write("t,x,s,m,dmu,newm\n")

trainingPhase = np.arange(dt,ttrain+dt,dt)
for t in trainingPhase:
 medium.updateNodes(sm,krej,kdeg,dt)
 m = (math.cos(t/2.0) / 2.0)
 m = (m+1.0) / 2.0 
 robot.MotorUpdate(m)
 robot.PositionUpdate(dt)
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1+robot.m)/2) - m0])
 medium.addNode(sm,v,kt,tba)
 m0 = (1+robot.m)/2
 s0 = robot.s
 sm = SensorimotorState([s0],[m0])
 time.append(t)
 position.append(robot.x)
 sensor.append(s0)
 motor.append(m0) 
 influence = medium.influence(sm,kd,kw)
 w = str(t)+","+str(robot.x)+","+str(robot.s)+","+str(robot.m)+","+str(influence[0])+","+str(robot.m + influence[0]*dt)+"\n"
 tfile.write(w)

##### mapping influence of active nodes after training

trfile = open("test4_influence_after_training.csv","w")
trfile.write("s,m,ds,dm\n")

for mot in np.arange(0.02,0.98,0.02):
 for sen in np.arange(0.02,0.98,0.02):
  a = SensorimotorState([sen],[mot])
  mu = medium.influence(a,kd,kw)
  xt = math.sqrt((1/sen)-1)
  nmot = mot + dt * mu[0]
  xt = xt + dt * (nmot +1) / 2 
  nsen = 1 / (1 + (xt)**2)
  w = str(sen)+","+str(mot)+","+str(nsen - sen)+","+str(nmot - mot)+"\n"
  trfile.write(w)

trfile.close()

### medium takes control 
mediumControlPhase1 = np.arange(ttrain+dt,tpert+dt,dt)
mediumControlPhase2 = np.arange(tpert+dt,tcontrol+dt,dt)

for t in mediumControlPhase1:
 medium.updateNodes(sm,krej,kdeg,dt)
 influence = medium.influence(sm,kd,kw)
 w = str(t)+","+str(robot.x)+","+str(robot.s)+","+str(robot.m)+","+str(influence[0])+","+str(robot.m + influence[0]*dt)+"\n"
 tfile.write(w)
 nm = ((1+robot.m)/2) + influence[0]*dt*ampFactor
 robot.MotorUpdate(nm)
 robot.PositionUpdate(dt)
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1+robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1+robot.m)/2
 s0 = robot.s
 sm = SensorimotorState([s0],[m0])
 time.append(t)
 position.append(robot.x)
 sensor.append(s0)
 motor.append(m0)

robot.PositionUpdate(dt,True,-2.5)
robot.SensorUpdate(light)
medium.addNode(sm,v)
m0 = (1+robot.m)/2
s0 = robot.s
sm = SensorimotorState([s0],[m0])

for t in mediumControlPhase2:
 medium.updateNodes(sm,krej,kdeg,dt)
 influence = medium.influence(sm,kd,kw)
 w = str(t)+","+str(robot.x)+","+str(robot.s)+","+str(robot.m)+","+str(influence[0])+","+str(robot.m + influence[0]*dt)+"\n"
 tfile.write(w)
 nm = ((1+robot.m)/2) + influence[0]*dt*ampFactor
 robot.MotorUpdate(nm)
 robot.PositionUpdate(dt)
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1+robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1+robot.m)/2
 s0 = robot.s
 sm = SensorimotorState([s0],[m0])
 time.append(t)
 position.append(robot.x)
 sensor.append(s0)
 motor.append(m0)

tfile.close()

##### mapping influence of active nodes once medium takes control

cfile = open("test4_influence_after_control.csv","w")
cfile.write("s,m,ds,dm\n")

for mot in np.arange(0.02,0.98,0.02):
 for sen in np.arange(0.02,0.98,0.02):
  a = SensorimotorState([sen],[mot])
  mu = medium.influence(a,kd,kw)
  xt = math.sqrt((1/sen)-1)
  nmot = mot + dt * mu[0]
  xt = xt + dt * (nmot +1) / 2 
  nsen = 1 / (1 + (xt)**2)
  w = str(sen)+","+str(mot)+","+str(nsen - sen)+","+str(nmot - mot)+"\n"
  cfile.write(w)

cfile.close()
 
##### plotting results
fig, ax = plt.subplots()
ax.plot(time, position)
ax.set(xlabel='time', ylabel='robot position',
       title='training (t<20) and medium-control (20<=t<35) phase')
ax.grid()
fig.savefig("test4_robot_position.png")
plt.show()
	
plt.scatter(motor,sensor,alpha = 0.5)
plt.xlabel("motor")
plt.ylabel("light sensor")
plt.savefig("test4_sm_states.png")
plt.show()

plt.scatter()
