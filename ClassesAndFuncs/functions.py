from math import atan, pi, cos, sin
from pygame import draw
from itertools import combinations

mesh_color = (100, 200, 100)


def neg(x):
    if x < 0:
        x += 180
        return x
    else:
        return x


def angle2(obj, x):
    a = 0
    if x < 0 and obj.Pos.x < 0:
        x += 180
        a = x
    else:
        a = x

    if obj.Pos.x < 0 and obj.Pos.y < 0 < x:
        a = x + 180

    if obj.Pos.x > 0 > obj.Pos.y and x < 0:
        a = x + 360

    return a


def angle(obj1, obj2):

    x1 = obj1.Pos.x
    y1 = obj1.Pos.y

    x2 = obj2.Pos.x
    y2 = obj2.Pos.y

    if x1 != x2:
        m = (y2 - y1) / (x2 - x1)

        return neg(atan(m) * (180 / pi))
    else:
        return 90


def radian(deg):
    return deg * (pi/180)


def deg(rad):
    return rad * (180/pi)


def transform_x(x):
    return round(x + 750)


def transform_y(y):
    return round(450 - y)


def coordinate_axes(win):
    draw.line(win, (100, 255, 100), (0, 450), (1500, 450))
    draw.line(win, (100, 255, 100), (750, 0), (750, 900))


def display_Pos(obj, win):
    draw.line(win, (255, 10, 10), (750, 450), (transform_x(obj.Pos.x), transform_y(obj.Pos.y)))


def display_Vel(obj, win):
    obj.Vel = ((1/20) * obj.Vel + obj.Pos)

    draw.line(win, (10, 255, 10), (transform_x(obj.Pos.x), transform_y(obj.Pos.y)),
                  (transform_x(obj.Vel.x), transform_y(obj.Vel.y)))

    obj.Vel = 20 * (obj.Vel - obj.Pos)


def display_Acc(obj, win):
    # print(obj.Acc.x)
    obj.Acc = ((1/60) * obj.Acc + obj.Pos)

    draw.line(win, (10, 10, 255), (transform_x(obj.Pos.x), transform_y(obj.Pos.y)),
                  (transform_x(obj.Acc.x), transform_y(obj.Acc.y)))
    
    obj.Acc = 60 * (obj.Acc - obj.Pos)


def circrot_coords1(obj):
    a = (transform_x(obj.Pos.x), transform_y(obj.Pos.y))

    return a


def circrot_coords2(obj):
    a = (transform_x(obj.Pos.x) + (obj.radius * cos(radian(obj.theta))), transform_y(obj.Pos.y) + (obj.radius * sin(radian(obj.theta))))

    return a


# ___functions drawing solid shapes___
def draw_circle(obj, win):
    draw.circle(win, obj.color, (transform_x(obj.Pos.x), transform_y(obj.Pos.y)), obj.radius)

    draw.line(win, (100, 20, 30), circrot_coords1(obj), circrot_coords2(obj), 2)


def draw_rect(obj, win):
    draw.rect(win, obj.color, (transform_x(obj.Pos.x), transform_y(obj.Pos.y), obj.width, obj.height))


# ___functions drawing meshes of different shapes___
def circle_mesh(obj, win):
    draw.arc(win, mesh_color, (transform_x(obj.Pos.x) - obj.radius, transform_y(obj.Pos.y) - obj.radius, obj.radius * 2, obj.radius * 2), 0.0, 2 * pi, width=1)


def rect_mesh(obj, win):
    draw.line(win, mesh_color, (transform_x(obj.Pos.x), transform_y(obj.Pos.y)), (transform_x(obj.Pos.x), transform_y(obj.Pos.y) + obj.height), width=1)

    draw.line(win, mesh_color, (transform_x(obj.Pos.x), transform_y(obj.Pos.y) + obj.height - 1), (transform_x(obj.Pos.x) + obj.width, transform_y(obj.Pos.y) + obj.height - 1), width=1)

    draw.line(win, mesh_color, (transform_x(obj.Pos.x) + obj.width, transform_y(obj.Pos.y) + obj.height), (transform_x(obj.Pos.x) + obj.width, transform_y(obj.Pos.y)), width=1)

    draw.line(win, mesh_color, (transform_x(obj.Pos.x) + obj.width, transform_y(obj.Pos.y)), (transform_x(obj.Pos.x), transform_y(obj.Pos.y)), width=1)


def PairObjectList(objects):
    n = []
    for i in combinations(objects, 2):
        n.append(i)
    
    return n
