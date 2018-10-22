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
sm = SensorimotorState([robot.s],[(1 + robot.m)/2])

time = [0]
position = [robot.x]
sensor = [s0]
motor = [m0]
### training stage (t = 0, to t = 20)

for t in range(1,21):
 medium.updateNodes(sm)
 m = math.cos(t/2.0)/2.0
 robot.MotorUpdate(m)
 robot.MotorAction()
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1 + robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1 + robot.m)/2 
 s0 = robot.s
 sm = SensorimotorState([robot.s],[(1+robot.m)/2])
 time.append(t)
 position.append(robot.x)
 sensor.append(robot.s)
 motor.append((1+robot.m)/2) 

### medium takes control (t = 21, to t = 35)
for t in range(21,36):
 medium.updateNodes(sm)
 robot.MotorUpdate(2*medium.influence(sm)[0] - 1)
 robot.MotorAction()
 robot.SensorUpdate(light)
 v = np.array([robot.s - s0,((1 + robot.m)/2) - m0])
 medium.addNode(sm,v)
 m0 = (1 + robot.m)/2 
 s0 = robot.s
 sm = SensorimotorState([robot.s],[(1+robot.m)/2])
 time.append(t)
 position.append(robot.x)
 sensor.append(robot.s)
 motor.append((1+robot.m)/2) 
##### plotting results
fig, ax = plt.subplots()
ax.plot(time, position)
ax.set(xlabel='time', ylabel='robot position',
       title='trainging phase (t in [0,20])')
ax.grid()
fig.savefig("test.png")
plt.show()

plt.scatter(motor,sensor,alpha = 0.5)
plt.xlabel("motor")
plt.ylabel("light sensor")
plt.show()
