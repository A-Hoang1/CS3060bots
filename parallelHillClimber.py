from solution import SOLUTION
import constants as c
import copy
import glob
import os
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        print("--- Initializing Parallel Hill Climber ---")
        print("Cleaning up previous run files...")
        patterns_to_delete = [
            "brain*.nndf",
            "fitness*.txt",
            "touch_sensor_matrix*.npy",
            "body.urdf",
            "world.sdf" 
        ]
        for pattern in patterns_to_delete:
            files_to_delete = glob.glob(pattern)
            for f_path in files_to_delete:
                try:
                    os.remove(f_path)
                except OSError as e:
                    print(f"    Error deleting file {f_path} : {e.strerror}")
        print("Cleanup complete.")
        self.nextAvailableID = 0
        self.parents = {}
        self.children = {}

        print(f"Creating initial population of size {c.populationSize}...")
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        print(f"Initial population created. nextAvailableID is now {self.nextAvailableID}")
        print("--- Initialization Complete ---")

        
        # print("Initial population (should show unique IDs):")
        # for key, sol in self.parents.items():
        #     print(f"Key: {key}, Solution ID: {sol.myID}")

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
            # solutions[key].Start_Simulation("GUI")
        
        time.sleep(0.5)

        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        
        for g in range(c.numOfGens):
            self.Evolve_For_One_Generation()
            self.Print()
            self.Select()
            
        self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.children = {}
            
        for key in self.parents:
            self.Spawn(key)
            self.Mutate()
            self.children[key] = self.child

        self.Evaluate(self.children)
    
    def Spawn(self, key):
        self.child = copy.deepcopy(self.parents[key])
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()
    
    def Print(self):
        print()
        for key in self.parents:
            print(f"Parent {key} fitness: {self.parents[key].fitness}   Child {key} fitness: {self.children[key].fitness}")
        print() 
    
    def Select(self):
        for key in self.parents:
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        best_key = max(self.parents.keys(), key=lambda k: self.parents[k].fitness)
        best_solution = self.parents[best_key]
        
        print(f"Showing best solution (ID: {best_solution.myID}) with fitness: {best_solution.fitness}")
        best_solution.Start_Simulation("GUI")

