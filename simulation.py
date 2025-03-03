import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0, 0, c.GRAVITY)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        # Simulation loop
        for t in range(c.STEPS):
            p.stepSimulation()
            time.sleep(1/60)

            self.robot.Sense(t)
            self.robot.Act(t)

        self.robot.Save_Sensor_Values
        self.robot.Save_Motor_Values
    def __del__(self):
        p.disconnect()
