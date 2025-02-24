import pybullet_data
import pybullet as p
import time
import pyrosim.pyrosim as pyrosim
import numpy
import os
import random

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeID = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotID = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotID)
steps = 1000
backLegSensorValues = numpy.zeros(steps)
frontLegSensorValues = numpy.zeros(steps)

xVals = numpy.linspace(0, 2*numpy.pi, steps)
rawSinVals = numpy.sin(xVals)
targetAngles = rawSinVals * (numpy.pi/4.0)

amplitude_back = numpy.pi/2.5
freq_back = 20
phaseOffset_back = -20

amplitude_front = numpy.pi/2.5
freq_front = 20.0
phaseOffset_front = 15

backLegMotorCommands = amplitude_back * numpy.sin(freq_back *xVals + phaseOffset_back)
frontLegMotorCommands = amplitude_front * numpy.sin(freq_front *xVals + phaseOffset_front)
# numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/backLegMotorCommands.npy", backLegMotorCommands)
# numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/frontLegMotorCommands.npy", frontLegMotorCommands)
# exit()


# simulate the world
for i in range(steps):
    p.stepSimulation()
    time.sleep(1/60)
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    randomBack_Angle = random.random()*numpy.pi - numpy.pi/2
    randomFront_Angle = random.random()*numpy.pi - numpy.pi/2

    pyrosim.Set_Motor_For_Joint(
        bodyIndex    = robotID,
        jointName    = b'Torso_BackLeg',   
        controlMode  = p.POSITION_CONTROL,
        targetPosition = backLegMotorCommands[i],            
        maxForce     = 20                 
    )

    pyrosim.Set_Motor_For_Joint(
    bodyIndex      = robotID,
    jointName      = b'Torso_FrontLeg',
    controlMode    = p.POSITION_CONTROL,
    targetPosition = frontLegMotorCommands[i],
    maxForce       = 20
    )


p.disconnect()

numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/backLegSensorValues.npy", backLegSensorValues)
numpy.save("C:/Users/2678d/PycharmProjects/CS3060bots/data/frontLegSensorValues.npy", backLegSensorValues)
print(backLegSensorValues)
print(frontLegSensorValues)
