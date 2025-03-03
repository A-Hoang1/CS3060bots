import pybullet as p
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.robotID = p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotID)

        self.sensors = {}
        self.motors = {}

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkname in pyrosim.linkNamesToIndices:
            self.sensors[linkname] = SENSOR(linkname)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for sensorObj in self.sensors.values():
            sensorObj.Get_Value(t)

    def Act(self, t):
        for motorObj in self.motors.values():
            motorObj.Set_Value(t, self)

    def Save_Sensor_Values(self):
        for sensorObj in self.sensors.values():
            sensorObj.Save_Values()

    def Save_Motor_Values(self):
        for motorObj in self.motors.values():
            motorObj.Save_Values()