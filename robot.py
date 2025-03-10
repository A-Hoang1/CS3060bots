import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c

from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self):
        self.robotID = p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotID)

        self.sensors = {}
        self.motors = {}

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        self.nn = NEURAL_NETWORK("brain.nndf")

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
        self.nn.Print()
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
                    targetPosition = desiredAngle,
                    maxForce       = c.MAX_FORCE
                )

                print(neuronName, jointName, desiredAngle)

        # for motorObj in self.motors.values():
        #     motorObj.Set_Value(t, self)

    def Save_Sensor_Values(self):
        for sensorObj in self.sensors.values():
            sensorObj.Save_Values()

    def Save_Motor_Values(self):
        for motorObj in self.motors.values():
            motorObj.Save_Values()