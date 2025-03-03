import numpy
import random

# Simulation steps & timing
STEPS = 1000
TIME_STEP = 1/60

# Gravity
GRAVITY = -9.8

# Motor parameters
AMPLITUDE_BACK      = numpy.pi / 4
FREQUENCY_BACK      = 2
PHASE_OFFSET_BACK   = 0

AMPLITUDE_FRONT     = numpy.pi / 4
FREQUENCY_FRONT     = 4
PHASE_OFFSET_FRONT  = 3.14

# Motor force
MAX_FORCE = 20
