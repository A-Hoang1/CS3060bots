import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

        self.fitness = 0
        # exit()

    def Start_Simulation(self, mode = "DIRECT"):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python simulate.py " + mode + " " + str(self.myID) + " >nul 2>&1")

    def Wait_For_Simulation_To_End(self):
        fitness_filename = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitness_filename):
            time.sleep(0.1)
        
        with open(fitness_filename, "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())
        print("Solution's fitness (ID " + str(self.myID) + "): ", self.fitness)
        os.system("del " + fitness_filename)

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomCol = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomCol] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # Torso 
        pyrosim.Send_Cube(name="Torso", 
                        pos=[0, 0, 1], 
                        size=[1, 1, 1]
                        )

        # BackLeg to Torso 
        pyrosim.Send_Joint(name="Torso_BackLeg",
                        parent="Torso", 
                        child="BackLeg", 
                        type="revolute", 
                        position=[0, -0.5, 1],
                        jointAxis="1 0 0"
                        )

        # BackLeg 
        pyrosim.Send_Cube(name="BackLeg", 
                        pos=[0, -0.5, 0], 
                        size=[0.2, 1, 0.2]
                        )

        # FrontLeg to Torso
        pyrosim.Send_Joint(name="Torso_FrontLeg", 
                        parent="Torso",
                        child="FrontLeg", 
                        type="revolute",
                        position=[0, 0.5, 1],
                        jointAxis="1 0 0"
                        )

        # FrontLeg 
        pyrosim.Send_Cube(name="FrontLeg", 
                        pos=[0, 0.5, 0],
                        size=[0.2, 1, 0.2]
                        )
        
        # LeftLeg to Torso
        pyrosim.Send_Joint(name="Torso_LeftLeg",
                        parent="Torso",
                        child="LeftLeg",
                        type="revolute",
                        position=[-0.5, 0, 1],
                        jointAxis="1 0 0") 
         
        # LeftLeg 
        pyrosim.Send_Cube(name="LeftLeg",
                        pos=[-0.5, 0, 0], 
                        size=[1, 0.2, 0.2])
        
        # RightLeg to Torso
        pyrosim.Send_Joint(name="Torso_RightLeg",
                        parent="Torso",
                        child="RightLeg",
                        type="revolute",
                        position=[0.5, 0, 1],
                        jointAxis="1 0 0") 
         
        # RightLeg 
        pyrosim.Send_Cube(name="RightLeg",
                        pos=[0.5, 0, 0], 
                        size=[1, 0.2, 0.2])
        
        # -- lower legs --
        # Front Lower Leg: attached to the FrontLeg.
        pyrosim.Send_Joint(name="Torso_FrontLowerLeg",
                        parent="FrontLeg",
                        child="FrontLowerLeg",
                        type="revolute",
                        position=[0, 1, 0],
                        jointAxis="1 0 0")
        
        pyrosim.Send_Cube(name="FrontLowerLeg", 
                          pos=[0, 0, -0.5], 
                          size=[0.2, 0.2, 1])
        
        # Back Lower Leg: attached to the BackLeg.
        pyrosim.Send_Joint(name="Torso_BackLowerLeg",
                        parent="BackLeg",
                        child="BackLowerLeg",
                        type="revolute",
                        position=[0, -1, 0],
                        jointAxis="1 0 0")
        
        pyrosim.Send_Cube(name="BackLowerLeg", 
                          pos=[0, 0, -0.5], 
                          size=[0.2, 0.2, 1])
        
        # Left Lower Leg: attached to the LeftLeg.
        pyrosim.Send_Joint(name="Torso_LeftLowerLeg",
                        parent="LeftLeg",
                        child="LeftLowerLeg",
                        type="revolute",
                        position=[-1, 0, 0],
                        jointAxis="1 0 0")
        
        pyrosim.Send_Cube(name="LeftLowerLeg", 
                          pos=[0, 0, -0.5],
                           size=[0.2, 0.2, 1])

        # Right Lower Leg: attached to RightLeg.
        pyrosim.Send_Joint(name="Torso_RightLowerLeg",
                        parent="RightLeg",
                        child="RightLowerLeg",
                        type="revolute",
                        position=[1, 0, 0],
                        jointAxis="1 0 0")
        
        pyrosim.Send_Cube(name="RightLowerLeg", 
                        pos=[0, 0, -0.5],
                        size=[0.2, 0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")


        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 1, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 2, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 3, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 4, jointName="Torso_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 5, jointName="Torso_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 6, jointName="Torso_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=c.numSensorNeurons + 7, jointName="Torso_RightLowerLeg")
        for curRow in range(c.numSensorNeurons):
            for curCol in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=curRow,
                                    targetNeuronName=curCol + c.numSensorNeurons,
                                    weight=self.weights[curRow][curCol])
        pyrosim.End()
    
    def Set_ID(self, newID):
        self.myID = newID

