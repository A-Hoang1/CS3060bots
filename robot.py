import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c

from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

import os

class ROBOT:
    def __init__(self, myID):
        self.myID = myID
        self.robotID = p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotID)

        self.sensors = {}
        self.motors = {}

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        self.nn = NEURAL_NETWORK("brain" + str(self.myID) + ".nndf")
        os.system("del brain" + str(self.myID) + ".nndf")

    def Prepare_To_Sense(self):
        for linkname in pyrosim.linkNamesToIndices:
            self.sensors[linkname] = SENSOR(linkname)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for sensorObj in self.sensors.values():
            sensorObj.Get_Value(t)

    def Think(self):
        # self.nn.Print()
        self.nn.Update()

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)

                pyrosim.Set_Motor_For_Joint(
                    bodyIndex      = self.robotID,
                    jointName      = jointName,
                    controlMode    = p.POSITION_CONTROL,
                    targetPosition = desiredAngle * c.motorJointRange,
                    maxForce       = c.MAX_FORCE
                )

               #  print(neuronName, jointName, desiredAngle)

        # for motorObj in self.motors.values():
        #     motorObj.Set_Value(t, self)

    def Save_Sensor_Values(self):
        for sensorObj in self.sensors.values():
            sensorObj.Save_Values()

    def Save_Motor_Values(self):
        for motorObj in self.motors.values():
            motorObj.Save_Values()
    
    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotID)
        basePosition = basePositionAndOrientation[0]
        zPosition = basePosition[2]

        tmp_filename = "tmp" + str(self.myID) + ".txt"
        final_filename = "fitness" + str(self.myID) + ".txt"
        
        with open(tmp_filename, "w") as f:
            f.write(str(zPosition))

        os.replace(tmp_filename, final_filename)