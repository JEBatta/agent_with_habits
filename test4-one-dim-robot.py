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
robot = Robot(-2.5)
robot.SensorUpdate(light)
medium = Medium()
m0 = (1 + robot.m)/2 
s0 = robot.s
sm = SensorimotorState([s0],[m0])

dt = 0.1
kd = 1000
kw = 0.0025
time = [0]
position = [robot.x]
sensor = [s0]
motor = [m0]
### training stage
trainingPhase = np.arange(dt,20+dt,dt)
for t in trainingPhase:
 medium.updateNodes(sm,dt)
 m = math.cos(t/2.0)/2.0
 robot.MotorUpdate(m)
 robot.MotorAction(dt)
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1 + robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1 + robot.m)/2 
 s0 = robot.s
 sm = SensorimotorState([s0],[m0])
 time.append(t)
 position.append(robot.x)
 sensor.append(s0)
 motor.append(m0) 

#nodesS = [n.smstate.state[0] for n in medium.nodes if n.activation]
#nodesM = [n.smstate.state[1] for n in medium.nodes if n.activation]
#plt.scatter(nodesM,nodesS,alpha = 0.5)
#plt.xlabel("active nodes motor")
#plt.ylabel("active nodes sensor")
#plt.savefig("test4_active_nodes.png")
#plt.show()

#robot.SetPosition(-1*math.sqrt(abs(1/(max(sensor) - 1))))
#robot.SensorUpdate(light)

### medium takes control 
mediumControlPhase = np.arange(20+dt,35+dt,dt)
for t in mediumControlPhase:
 medium.updateNodes(sm,dt)
 influence = 2*medium.influence(sm,kd,kw)[0] - 1
 robot.MotorUpdate(influence)
 robot.MotorAction(dt)
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1 + robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1 + robot.m)/2 
 s0 = robot.s
 sm = SensorimotorState([s0],[m0])
 time.append(t)
 position.append(robot.x)
 sensor.append(s0)
 motor.append(m0)
 
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
