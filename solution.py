import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time

class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

        self.fitness = 0
        # exit()

    def Start_Simulation(self, mode = "DIRECT"):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python simulate.py " + mode + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        fitness_filename = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitness_filename):
            time.sleep(0.1)
        
        with open(fitness_filename, "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())
        print("Solution's fitness (ID " + str(self.myID) + "): ", self.fitness)
        os.system("del " + fitness_filename)

    def Mutate(self):
        randomRow = random.randint(0, 2)
        randomCol = random.randint(0, 1)
        self.weights[randomRow, randomCol] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # Torso 
        pyrosim.Send_Cube(name="Torso", 
                        pos=[1.5, 0, 1.5], 
                        size=[1, 1, 1]
                        )

        # BackLeg to Torso 
        pyrosim.Send_Joint(name="Torso_BackLeg",
                        parent="Torso", 
                        child="BackLeg", 
                        type="revolute", 
                        position=[1, 0, 1]
                        )

        # BackLeg 
        pyrosim.Send_Cube(name="BackLeg", 
                        pos=[-0.5, 0, -0.5], 
                        size=[1, 1, 1]
                        )

        # FrontLeg to Torso
        pyrosim.Send_Joint(name="Torso_FrontLeg", 
                        parent="Torso",
                        child="FrontLeg", 
                        type="revolute",
                        position=[2.0, 0, 1]
                        )

        # FrontLeg 
        pyrosim.Send_Cube(name="FrontLeg", 
                        pos=[0.5, 0, -0.5],
                        size=[1, 1, 1]
                        )

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        for curRow in range(3):
            for curCol in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=curRow,
                                    targetNeuronName=curCol + 3,
                                    weight=self.weights[curRow][curCol])
        pyrosim.End()
        time.sleep(0.2)
    
    def Set_ID(self, newID):
        self.myID = newID

