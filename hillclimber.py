from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate("DIRECT")
        for curGen in range (c.numOfGens):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

        # print("Parent Weights:\n", self.parent.weights)
        # print("Child Weights:\n", self.child.weights)
        # exit()

    def Print(self):
        print("Parent fitness:", self.parent.fitness, "   Child fitness:", self.child.fitness)

    def Select(self):
        if self.parent.fitness < self.child.fitness:
            self.parent = self.child

        # print("Parent Fitness:", self.parent.fitness)
        # print("Child Fitness: ", self.child.fitness)
        # exit()

    def Show_Best(self):
        print("Showing final best solution in GUI mode: ")
        self.parent.Evaluate("GUI")
