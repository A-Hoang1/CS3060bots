import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        # self.Prepare_To_Act()

    # def Prepare_To_Act(self):
    #     self.amplitude = c.AMPLITUDE_BACK
    #     self.frequency = c.FREQUENCY_BACK
    #     self.offset = c.PHASE_OFFSET_BACK

    #     if b'Front' in self.jointName:
    #         self.frequency = c.FREQUENCY_BACK / 2.0

    #     xVals = numpy.linspace(0, 2 * numpy.pi, c.STEPS)
    #     self.motorValues = self.amplitude * numpy.sin(self.frequency * xVals + self.offset)

    def Set_Value(self, desiredAngle, robot):
        jointName = jointName.decode("utf-8")
        pyrosim.Set_Motor_For_Joint(
            bodyIndex      = robot.robotID,
            jointName      = jointName,
            controlMode    = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce       = c.MAX_FORCE
        )

    # def Save_Values(self):
    #     filename = f"data/{self.linkName}_MotorValues.npy"
    #     numpy.save(filename, self.motorValues)
    #     print(f"Motor values saved to: {filename}")