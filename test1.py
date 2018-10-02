from agent_system import SensorimotorState
from agent_system import Node
from agent_system import Medium

a = SensorimotorState([0],[0])
Na = Node(a,0)
b = SensorimotorState([0],[1])
Nb = Node(b,0)
print(Na.distance(Nb,100))
print(Na.sigmoidalWeight())
Na.weight=1000
print(Na.sigmoidalWeight())
