import sys
sys.path.insert(0, "E:\\my_python\\pythonprojects\\PyBox\\ClassesAndFuncs")

from classes import *

# Physical constants
g = -25000
G = 6.67 * 10 ** (-11)
coeff_fric = 0.0002
e = 0.5
dt = 0.001  # time step for euler method
ground_height = 10
F_drag = Vector(0, 0)
F_external = Vector(0, 0)
Fm = Vector(50000, 200000)
F_friction = Vector(0, 0)
resultant_Force = Vector(0, 0)

# Graphics constants
display_size = (1500, 900)  # (pixels along the width, pixels along the height)
