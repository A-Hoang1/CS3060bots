import pybullet as p
import time

physicsClient = p.connect(p.GUI)

# disabling the sidebar
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# simulate the world
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)
    print(i)

p.disconnect()
