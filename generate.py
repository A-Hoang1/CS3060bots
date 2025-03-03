import pyrosim.pyrosim as pyrosim

def Create_World():
    """Creating a minimal world with a single block."""
    pyrosim.Start_SDF("world.sdf")
    # Move world block to background
    pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.5], size=[1, 1, 1])
    pyrosim.End()

def Create_Robot():
    """Creating a three-link, two-joint robot."""
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
def main():
    Create_World()
    Create_Robot()

if __name__ == "__main__":
    main()
