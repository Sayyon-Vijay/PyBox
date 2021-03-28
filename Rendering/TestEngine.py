import sys
sys.path.append("E:\\my_python\\pythonprojects\\PyBox")

from Physics.integrator import *
from datetime import datetime
from time import time
import pygame as pyg


mainloop = True
show_vectors_log = False
user_input1 = ''
user_input2 = ''
user_input3 = ''

if show_vectors_log:
    print("\nENTER INFO AS A TUPLE\n")
    user_input1 = input("Which vector should be visisble?(Pos, Vel, Acc):- ")
    user_input2 = input("Do you want to log position, velocity and acceleration to the console?(Y/N):- ").upper()
    user_input3 = input("Do you want to enable the coordinate axes on screen?(Y/N):- ").upper()


def disp_vec_log():
    if user_input1 == "(Pos)":
        display_Pos(circ, win)

    if user_input1 == "(Vel)":
        display_Vel(circ, win)

    if user_input1 == "(Acc)":
        display_Acc(circ, win)

    if user_input1 == "(Pos, Vel)":
        display_Pos(circ, win)
        display_Vel(circ, win)

    if user_input1 == "(Pos, Acc)":
        display_Pos(circ, win)
        display_Acc(circ, win)

    if user_input1 == "(Vel, Acc)":
        display_Vel(circ, win)
        display_Acc(circ, win)
    
    if user_input1 == "(Pos, Vel, Acc)":
        display_Pos(circ, win)
        display_Vel(circ, win)
        display_Acc(circ, win)

    if user_input2 == "Y":
        print("position:", (round(circ.Pos.x), round(circ.Pos.y)), "velocity:",
              (round(circ.Vel.x), round(circ.Vel.y)), "Acceleration:", (round(circ.Acc.x), round(circ.Acc.y)),
              end=" (" + str(datetime.now().time()) + ")\n")


pyg.init()
win = pyg.display.set_mode(display_size)
pyg.display.set_caption("PyBox")

# mouse

# __objects__
# collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color, radius
circ1 = Circle(True, False, 5, (0, 0), (0, 0), (0, 0), 0, 0, 0, (200, 20, 20), 50)
circ2 = Circle(True, False, 5, (1450, 0), (0, 0), (0, 0), 0, 0, 0, (20, 20, 200), 50)


def draw():
    draw_circle(circ1, win)
    draw_circle(circ2, win)

    pyg.draw.rect(win, (100, 50, 0), (0, 890, 1500, 10))  # floor
    
    if user_input3 == "Y":
        coordinate_axes(win)


list1 = PairObjectList(Objects.object_list)


def main():
    global mainloop
    # game loop
    while mainloop:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                mainloop = False

        # ___movements___
        movement(circ1, pyg.K_w, pyg.K_s, pyg.K_a, pyg.K_d, pyg.K_SPACE)
        movement(circ2, pyg.K_UP, pyg.K_DOWN, pyg.K_LEFT, pyg.K_RIGHT, pyg.K_LSHIFT)
        # print((circ.Pos.x, circ.Pos.y))

        win.fill((0, 0, 0))

        # ___rotation___

        # ___boundaries___
        boundary(circ1)
        boundary(circ2)

        # ___collisions___
        circ_collision(list1)

        # ___gravity___
        gravity(list1)

        # ___friction___

        # ___object animation___
        draw()

        # ___logging___
        if show_vectors_log:
            disp_vec_log()

        pyg.display.update()

    pyg.quit()


# this (__name__) line of code is useful because now people can use this physics engine for making games or something
if __name__ == "__main__":
    main()