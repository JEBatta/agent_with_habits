# agent_with_habits
This project contain python classes to simulate an Agent Based Model (ABM) in which agents have a way to develop habits based on patterns of sensorimotor behavior. The basis of this work is the Iterant Deformable Sensorimotor Medium (IDSM) described in Egbert &amp; Barandarian (2014) (doi: 10.3389/fnhum.2014.00590). The IDSM is a pseudo-network whose nodes have assignated a particular state of the sensorimotor space (the space created by the possible combinations of perceptions and motor responses of a robot/agent) and a velocity (rate of change between states). Then each node represents a potential action that agents can perform. How accesible this actions are depends on how frequently this action have been done in the (not too distant) past.

This repository contains python classes and programms to reproduce four results described in (Egbert & Barandarian 2014):
1. test1. Influence of a single node 
2. test2. Influence of four nodes
3. test3. Influence of a medium "frozen" at a given time
4- test4. Training and control of IDSM of one-dimentional robot with one motor and a light sensor.

Each folder contains the codes to create figures.
