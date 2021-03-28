import sys
sys.path.insert(0, "E:\\my_python\\pythonprojects\\PyBox\\ClassesAndFuncs")

from ClassesAndFuncs.classes import *

# Physical constants 6.67 * 10 ** (-11)
g = -25000
G = 2000000
coeff_fric = 0.0002
e = 0.5
dt = 0.001  # time step for euler method
ground_height = 10
F_drag = Vector(0, 0)
Fm = Vector(50000, 20000) # need to multiply the y component of force by 10, it's 1/10th of the normal force because of no gravity 
F_friction = Vector(0, 0)
resultant_Force = Vector(0, 0)

# Graphics constants
display_size = (1500, 900)  # (pixels along the width, pixels along the height)
