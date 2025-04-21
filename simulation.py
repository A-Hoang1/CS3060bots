import pybullet as p
import pybullet_data
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import os # Good practice to import os if using it (e.g., in Write_Touch_Sensor_Matrix if uncommented)

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        # Store the solution ID, accessible via self.robot.myID later
        # self.solutionID = solutionID # Not strictly needed if we use self.robot.myID

        if directOrGUI.upper() == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            # Connect in GUI mode
            self.physicsClient = p.connect(p.GUI)
            # Ensure rendering is enabled in GUI mode
            p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)

        # Hide default GUI elements for a cleaner view if GUI is used
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, c.GRAVITY)

        self.directOrGUI = directOrGUI # Store mode
        self.world = WORLD()
        self.robot = ROBOT(solutionID) # Create the robot instance

        # --- NEW: Initialize list to store Z positions ---
        self.z_positions = []
        # --- End New ---

    def Run(self):
        """Runs the simulation loop, recording Z positions."""
        for t in range(c.STEPS):
            p.stepSimulation()

            # --- NEW: Record Base Link Z Position ---
            try:
                # Get position [x,y,z] and orientation [x,y,z,w] of the base link
                basePos, baseOrn = p.getBasePositionAndOrientation(self.robot.robotID)
                self.z_positions.append(basePos[2]) # Append Z-coordinate (index 2)
            except Exception as e:
                # Handle potential errors if robot ID is invalid (e.g., simulation crashed)
                print(f"ERROR in Run step {t} for robot {self.robot.myID}: Cannot get base position - {e}")
                self.z_positions.append(0) # Append a default value (e.g., 0) on error
            # --- End New ---

            # Perform robot's sense-think-act cycle
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)

            # Add delay only if in GUI mode for visualization
            if self.directOrGUI.upper() != "DIRECT":
                time.sleep(1/60.) # Approx 60 fps visualization

        # --- NEW: Save Z-position data after simulation ends ---
        self.Save_Z_Data()
        # --- End New ---

        # Calls to save raw sensor/motor values (These methods need '()' to be called)
        # If implemented in ROBOT/SENSOR/MOTOR classes, call like:
        # self.robot.Save_Sensor_Values()
        # self.robot.Save_Motor_Values()

    # --- NEW: Method to save Z-position data ---
    def Save_Z_Data(self):
        """Saves the recorded Z-positions to a .npy file."""
        filename = f"z_pos{self.robot.myID}.npy"
        try:
            z_array = np.array(self.z_positions)
            np.save(filename, z_array)
            # print(f"Z-position data saved to: {filename}") # Optional confirmation print
        except Exception as e:
            print(f"ERROR: Could not save Z-position data for solution {self.robot.myID} to {filename}: {e}")
    # --- End New ---


    def Write_Touch_Sensor_Matrix(self):
        """Calculates and optionally saves the binary touch sensor matrix."""
        # This might still be called by simulate.py launcher script.
        sensor_matrix = []
        for sensorName, sensorObj in self.robot.sensors.items():
            # Ensure sensorObj.values exists and has the correct length
            if hasattr(sensorObj, 'values') and len(sensorObj.values) == c.STEPS:
                 sensor_matrix.append(sensorObj.values)
            else:
                 print(f"Warning: Sensor {sensorName} for robot {self.robot.myID} missing or has incorrect data length.")
                 # Append zeros or handle appropriately if a sensor fails
                 sensor_matrix.append(np.zeros(c.STEPS)) # Append zeros as placeholder

        if not sensor_matrix: # Handle cases where no sensors exist
             print(f"Warning: No sensor data found for solution {self.robot.myID} in Write_Touch_Sensor_Matrix.")
             return

        try:
            sensor_matrix = np.array(sensor_matrix)
            # Convert sensor values to binary: 1 for contact, -1 for no contact
            binary_matrix = np.where(sensor_matrix > 0, 1, -1)

            # Optional: Print the matrix for debugging if needed
            # print("Touch sensor binary matrix for solution", self.robot.myID, ":")
            # print(binary_matrix)

            filename = f"touch_sensor_matrix{self.robot.myID}.npy"
            # --- MODIFIED: Comment out saving if not needed for fitness ---
            # np.save(filename, binary_matrix)
            # print(f"Touch sensor matrix saved as {filename}")
            # --- End Modification ---
            # If you *do* want this file saved, just uncomment the np.save line above.
        except Exception as e:
            print(f"ERROR: Failed to process or save touch sensor matrix for robot {self.robot.myID}: {e}")


    def __del__(self):
        # Destructor: Disconnect from physics engine when simulation object is deleted
        try:
            # Check if physics client connection exists before disconnecting
            if hasattr(self, 'physicsClient') and p.getConnectionInfo(self.physicsClient)['isConnected']:
                 p.disconnect(physicsClientId=self.physicsClient)
        except Exception as e:
            # Gracefully handle potential errors during disconnect
            # print(f"Note: Error during PyBullet disconnect: {e}")
            pass

    def Get_Fitness(self):
        # This method is now obsolete as fitness is calculated in solution.py
        # based on the z_pos<ID>.npy file.
        # It originally called robot.Get_Fitness() which saved Z pos to fitness<ID>.txt
        pass # Does nothing

