import numpy
import random

# Simulation steps & timing
STEPS = 600
TIME_STEP = 1/60

# Gravity
GRAVITY = -9.8

# Motor parameters
AMPLITUDE_BACK      = numpy.pi / 4
FREQUENCY_BACK      = 2
PHASE_OFFSET_BACK   = 3.14

AMPLITUDE_FRONT     = numpy.pi / 4
FREQUENCY_FRONT     = 4
PHASE_OFFSET_FRONT  = 3.14

# Motor force
MAX_FORCE = 20

# number of generations
numOfGens = 200

# populationSize
populationSize = 20

# number of sensor and motor neurons
numSensorNeurons = 9
numMotorNeurons = 8

# motorJoint range
motorJointRange = numpy.pi / 4

