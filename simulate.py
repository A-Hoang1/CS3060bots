import sys
from simulation import SIMULATION

if len(sys.argv) < 3:
    sys.exit(1)

mode = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(mode, solutionID)
simulation.Run()
simulation.Write_Touch_Sensor_Matrix()
