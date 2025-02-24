# import numpy as np
# import matplotlib.pyplot as plt

# # Load sensor data
# backLegSensorValues = np.load("data/backLegSensorValues.npy")
# frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

# # Print the loaded values
# print("Back Leg Sensor Values:", backLegSensorValues)
# print("Front Leg Sensor Values:", frontLegSensorValues)

# # Plot sensor values
# plt.plot(backLegSensorValues, label="Back Leg Sensor", linewidth=1, linestyle='solid', color='purple')
# plt.plot(frontLegSensorValues, label="Front Leg Sensor", linewidth=2, linestyle='dashed', color='gold')
# plt.xlabel("Time Step")
# plt.ylabel("Touch Sensor Value")
# plt.title("BackLeg & FrontLeg Touch Sensor Data")
# plt.legend()
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# targetAngles = np.load("data/targetAngles.npy")
# plt.plot(targetAngles, marker='o', label="Motor Angles")
# plt.xlabel("Index")
# plt.ylabel("Angle (radians)")
# plt.title("Generated Motor Angles")
# plt.legend()
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Suppose you saved these arrays from simulate.py:
backLegAngles  = np.load("data/backLegMotorCommands.npy")
frontLegAngles = np.load("data/frontLegMotorCommands.npy")

plt.plot(backLegAngles,  label="Back Leg",  color="red")
plt.plot(frontLegAngles, label="Front Leg", color="blue")
plt.title("Motor Commands for Back & Front Legs")
plt.xlabel("Time Step")
plt.ylabel("Angle (radians)")
plt.legend()
plt.show()

