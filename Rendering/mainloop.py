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
        display_Pos(circ1, win)

    if user_input1 == "(Vel)":
        display_Vel(circ1, win)

    if user_input1 == "(Acc)":
        display_Acc(circ1, win)

    if user_input1 == "(Pos, Vel)":
        display_Pos(circ1, win)
        display_Vel(circ1, win)

    if user_input1 == "(Pos, Acc)":
        display_Pos(circ1, win)
        display_Acc(circ1, win)

    if user_input1 == "(Vel, Acc)":
        display_Vel(circ1, win)
        display_Acc(circ1, win)
    
    if user_input1 == "(Pos, Vel, Acc)":
        display_Pos(circ1, win)
        display_Vel(circ1, win)
        display_Acc(circ1, win)

    if user_input2 == "Y":
        print("position:", (round(circ1.Pos.x), round(circ1.Pos.y)), "velocity:",
              (round(circ1.Vel.x), round(circ1.Vel.y)), "Acceleration:", (round(circ1.Acc.x), round(circ1.Acc.y)),
              end=" (" + str(datetime.now().time()) + ")\n")


pyg.init()
win = pyg.display.set_mode(display_size)
pyg.display.set_caption("PyBox")

# mouse

# __objects__
load(Circle)

# ctrl, collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color, radius
circ1 = Circle(True, True, True, 5, (0, 100), (0, 0), (0, 0), 0, 0, 0, (20, 20, 20), 50)
circ2 = Circle(True, True, True, 5, (1450, -100), (0, 0), (0, 0), 0, 0, 0, (20, 20, 200), 50)


# obj_maker(10, 101, 20)

print(Objects.object_list)

def draw():
    draw_circ(Objects.object_list, win)

    pyg.draw.rect(win, (100, 50, 0), (0, 890, 1500, 10))  # floor
    
    if user_input3 == "Y":
        coordinate_axes(win)


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
        move(Objects.object_list)
        # print((circ.Pos.x, circ.Pos.y))

        win.fill((0, 0, 0))
        
        # ___rotation___


        # ___boundaries___
        boundary(Objects.object_list)

        # ___collisions___
        circ_collision(Objects.object_list)

        # ___gravity___
        gravity(PairObjectList(Objects.object_list))

        # ___friction___


        # ___object animation___
        draw()

        # ___other___
        save(Circle)

        # ___logging___
        if show_vectors_log:
            disp_vec_log()

        pyg.display.update()

    pyg.quit()


# this (__name__) line of code is useful because now people can use this physics engine for making games or use it as a game
if __name__ == "__main__":
    main()



