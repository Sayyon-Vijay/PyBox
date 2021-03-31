from pygame import key

import sys
sys.path.append("E:\\my_python\\pythonprojects\\PyBox\\Physics")

from Physics.constants import *
# from extras.funcs import angle, neg, transform_x, transform_y


# This function handles movement for individual objects
def movement(obj, up, down, left, right, extra):
    global resultant_Force
    keys = key.get_pressed()

    obj.Acc.x = 0
    obj.Acc.y = 0

    if keys[left]:
        obj.F_move.x = -Fm.x

    if keys[right]:
        obj.F_move.x = Fm.x

    if keys[up]:
        obj.F_move.y = Fm.y

    if keys[down]:
        obj.F_move.y = -Fm.y

    if keys[extra]:
        obj.Vel.y = 4500 * 0
        obj.Vel.x = 3000 * 0

    resultant_Force = obj.Fg + obj.F_move + obj.F_g + F_drag + obj.F_external  # getting the resultant force

    obj.Acc = resultant_Force * (1 / obj.mass)  # getting acceleration from force

    obj.Vel += obj.Acc * dt  # getting velocity from acceleration

    obj.Pos += obj.Vel * dt  # getting position from velocity

    obj.F_move.x = 0
    obj.F_move.y = 0


def move(obj_list):
    global resultant_Force

    for obj in obj_list:
        if not obj.ctrl:
            keys = key.get_pressed()

            obj.Acc.x = 0
            obj.Acc.y = 0

            resultant_Force = obj.Fg + obj.F_move + obj.F_g + F_drag + obj.F_external  # getting the resultant force

            obj.Acc = resultant_Force * (1 / obj.mass)  # getting acceleration from force

            obj.Vel += obj.Acc * dt  # getting velocity from acceleration

            obj.Pos += obj.Vel * dt  # getting position from velocity

            obj.F_move.x = 0
            obj.F_move.y = 0


# This function makes sure that the object doesn't go outside the boundaries
def boundary(obj_list):
    for obj in obj_list:
        if isinstance(obj, Circle):
            if obj.Pos.x < -750 + obj.radius or obj.Pos.x > 750 - obj.radius:
                obj.Pos.x = max(-750 + obj.radius, min(750 - obj.radius, obj.Pos.x))
                obj.Vel.x = 0

            if obj.Pos.y < (-450 + ground_height + obj.radius) or obj.Pos.y > 450 - obj.radius:
                obj.Pos.y = max((-450 + ground_height + obj.radius), min(450 - obj.radius, obj.Pos.y))
                obj.Vel.y = 0
        else:
            if obj.n >= 3:
                x_coords, y_coords = list(zip(*obj.points))[0], list(zip(*obj.points))[1]
                max_x = max(x_coords) + obj.Pos.x
                min_x = min(x_coords) + obj.Pos.x
                if max_x > display_size[0] / 2 or min_x < -display_size[0] / 2:
                    obj.Pos.x = max(-(display_size[0] / 2 - (obj.Pos.x - min_x)),
                                    min((display_size[0] / 2 - (max_x - obj.Pos.x)), obj.Pos.x))
                    obj.Vel.x = 0

                max_y = max(y_coords) + obj.Pos.y
                min_y = min(y_coords) + obj.Pos.y
                if max_y > display_size[1] / 2 or min_y < -(display_size[1] / 2 - ground_height):
                    obj.Pos.y = max(-(display_size[1] / 2 - ground_height - (obj.Pos.y - min_y)),
                                    min(display_size[1] / 2 - (max_y - obj.Pos.y), obj.Pos.y))
                    obj.Vel.y = 0
            else:
                pass


def rect_boundary(obj):
    if obj.Pos.x < -750 or obj.Pos.x > 750 - obj.width:
        obj.Pos.x = max(-750, min(750 - obj.width, obj.Pos.x))
        obj.Vel.x = 0

    if obj.Pos.y < (-450 + obj.height + ground_height) or obj.Pos.y > 450:
        obj.Pos.y = max((-450 + obj.height + ground_height), min(450, obj.Pos.y))
        obj.Vel.y = 0


# The function that handles friction for individual objects
def friction(obj, center):
    F_friction.x = -1 * coeff_fric * obj.mass * g

    if isinstance(obj, Circle):
        if obj.Pos.y <= -390:
            if obj.Acc.x == 0:
                if round(obj.Vel.x) == 0:
                    obj.Vel.x = 0

                if round(obj.Vel.x) > 0:
                    obj.Acc.x = -1 * F_friction.x / obj.mass
                    obj.Vel.x += obj.Acc.x

                    if obj.Vel.x < 0:
                        obj.Vel.x = 0
                        obj.Acc.x = 0

                if round(obj.Vel.x) < 0:
                    obj.Acc.x = F_friction.x / obj.mass
                    obj.Vel.x += obj.Acc.x

                    if obj.Vel.x > 0:
                        obj.Vel.x = 0
                        obj.Acc.x = 0
            elif obj.F_move.x > 0:
                obj.F_move -= F_friction

    else:
        if obj.Pos.y <= -450 + ground_height + center:
            if obj.Acc.x == 0:
                if round(obj.Vel.x) == 0:
                    obj.Vel.x = 0

                if round(obj.Vel.x) > 0:
                    obj.Acc.x = -1 * F_friction.x / obj.mass
                    obj.Vel.x += obj.Acc.x

                    if obj.Vel.x < 0:
                        obj.Vel.x = 0
                        obj.Acc.x = 0

                if round(obj.Vel.x) < 0:
                    obj.Acc.x = F_friction.x / obj.mass
                    obj.Vel.x += obj.Acc.x

                    if obj.Vel.x > 0:
                        obj.Vel.x = 0
                        obj.Acc.x = 0
            elif obj.F_move.x > 0:
                obj.F_move -= F_friction


def circle_rotation(obj, clock, counter):
    keys = key.get_pressed()
    obj.alpha = 0

    if keys[clock]:
        obj.torque = 1000

    if keys[counter]:
        obj.torque = -1000

    obj.alpha = obj.torque / obj.moment_inertia
    obj.omega += obj.alpha
    obj.theta += obj.omega

    obj.torque = 0


# _____collision functions_____

# function that handles the collision between circles
def circ_collision(objects):

    # Broad phase collision detection
    active_x = active(objects, "Pos.x")
    active_y = active(objects, "Pos.y")

    active_list = []

    for i in active_x:
        if i in active_x and i in active_y:
            active_list.append(i)

    # Narrow phase collision detection
    for i in active_list:
        if active_list.index(i) != len(active_list) - 1:
            obj2 = active_list[active_list.index(i) + 1][2]

            if i[2].collision and obj2.collision:
                radius1 = i[2].radius
                radius2 = obj2.radius

                distance = (i[2].Pos - obj2.Pos).mag()

                i[2].inside = obj2.inside = False

                if distance < i[2].radius + obj2.radius:
                    i[2].inside = obj2.inside = True

                    # __moving the circles__
                    i[2].Pos = obj2.Pos + (i[2].Pos - obj2.Pos).unit_vec() * (radius1 + radius2)
                    obj2.Pos = i[2].Pos + (obj2.Pos - i[2].Pos).unit_vec() * (radius1 + radius2)

                    # __handling collision__
                    if i[2].Vel.x != 0:
                        Vel1_angle = neg(atan(i[2].Vel.y / i[2].Vel.x) * (180/pi))
                    else:
                        Vel1_angle = 90
                    if obj2.Vel.x != 0:
                        Vel2_angle = neg(atan(obj2.Vel.y / obj2.Vel.x) * (180/pi))
                    else:
                        Vel2_angle = 90

                    line_angle = angle(i[2], obj2)

                    theta1 = abs(line_angle - Vel1_angle)
                    theta2 = abs(line_angle - Vel2_angle)

                    extra_component1 = i[2].Vel * sin(theta1)
                    extra_component2 = obj2.Vel * sin(theta2)

                    u1 = i[2].Vel * cos(theta1)  # component of the velocity vector of circle 1 along the line
                    u2 = obj2.Vel * cos(theta2)  # component of the velocity vector of circle 2 along the line

                    m1 = i[2].mass
                    m2 = obj2.mass

                    # component of the velocity vector of circle 1 along the line after collision
                    v1 = (u1*(m1 - e*m2) / (m1 + m2)) + (u2*m2*(1 + e)/(m1 + m2))

                    # component of the velocity vector of circle 2 along the line after collision
                    v2 = (u1*m1*(1 + e) / (m1 + m2)) + (u2*(m2 - m1*e) / (m1 + m2))

                    i[2].Vel = v1 + extra_component1
                    obj2.Vel = v2 + extra_component2



# function that handles collison between 2 rectangles
def rect_collision(obj1, obj2):
    x1 = transform_x(obj1.Pos.x)
    x2 = transform_x(obj2.Pos.x)

    y1 = transform_y(obj1.Pos.y)
    y2 = transform_y(obj2.Pos.y)

    x_distance = x1 - x2

    y_distance = y1 - y2

    if (-(obj1.height + obj2.height) < y_distance < obj2.height) and (-obj1.width < x_distance < obj2.width):
        return True


def point_rect_collison(obj1, obj2):
    x1 = transform_x(obj1.Pos.x)
    x2 = transform_x(obj2.Pos.x)

    y1 = transform_y(obj1.Pos.y)
    y2 = transform_y(obj2.Pos.y)

    x_distance = x1 - x2

    y_distance = y1 - y2

    if obj2.height >= y_distance >= 0 and obj2.width >= x_distance >= 0:
        return True


# _____Gravity_____

# a function that handles gravity between objects
def gravity(objects):
    for i in objects:
        if i[0].gravity and i[1].gravity: 
            m1 = i[0].mass
            m2 = i[1].mass

            d = sqrt((i[1].Pos.x - i[0].Pos.x) ** 2 + (i[1].Pos.y - i[0].Pos.y) ** 2)

            f = G*m1*m2 / d ** 2

            i[0].Fg = (i[1].Pos - i[0].Pos).unit_vec() * f
            i[1].Fg = (i[0].Pos - i[1].Pos).unit_vec() * f

    # print(obj1.Force_applied.coords())

