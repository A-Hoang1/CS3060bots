import pyrosim.pyrosim as pyrosim
# SDF file
pyrosim.Start_SDF("boxes.sdf")

# rows, columns
rows = 5
cols = 5

# blocks
blocks = 10

# shrink
shrink = 0.9

# dimensions
start_length = 1
start_width: int = 1
start_height = 1

# position for Box
x = 0
y = 0
z = start_height/2

# spacing
x_space = 1
y_space = 1

for row in range(rows):
    for col in range(cols):
        length = start_length
        width = start_width
        height = start_height

        x = col * x_space
        y = row * y_space
        z = height/2

        for i in range(blocks):
            pyrosim.Send_Cube(name=f"Box_{i}", pos=[x,y,z], size=[length,width,height])
            z += height
            length *= shrink
            width *= shrink
            height *= shrink

pyrosim.End()