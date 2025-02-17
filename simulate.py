import pybullet_data
import pybullet as p
import time
import pyrosim.pyrosim as pyrosim
import numpy
import os

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeID = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotID = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = numpy.zeros(100)
frontLegSensorValues = numpy.zeros(100)

# simulate the world
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

p.disconnect()

numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/frontLegSensorValues.npy", backLegSensorValues)
print(backLegSensorValues)
print(frontLegSensorValues)
