import numpy as np
import matplotlib.pyplot as plt

# Load sensor data
backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

# Print the loaded values
print("Back Leg Sensor Values:", backLegSensorValues)
print("Front Leg Sensor Values:", frontLegSensorValues)

# Plot sensor values
plt.plot(backLegSensorValues, label="Back Leg Sensor", linewidth=1, linestyle='solid', color='purple')
plt.plot(frontLegSensorValues, label="Front Leg Sensor", linewidth=2, linestyle='dashed', color='gold')
plt.xlabel("Time Step")
plt.ylabel("Touch Sensor Value")
plt.title("BackLeg & FrontLeg Touch Sensor Data")
plt.legend()
plt.show()
