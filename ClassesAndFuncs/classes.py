from math import ceil, floor, sqrt, sin, cos

import sys
sys.path.append("E:\\my_python\\pythonprojects\\PyBox\\ClassesAndFuncs")

from functions import *


class Vector:
    num_of_vectors = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        Vector.num_of_vectors += 1

    def __add__(self, b):
        return Vector(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Vector(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __rmul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __truediv__(self, b):
        if b != 0:
            return Vector(self.x / b, self.y / b)
        else:
            return Vector(self.x / 0.001, self.y / 0.001)

    def dot(self, b):
        return self.x * b.x + self.y * b.y

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def unit_vec(self):
        return self / self.mag()

    def coords(self):
        coord = (self.x, self.y)
        return coord


class Objects:
    object_list = []
    number_of_objects = len(object_list)

    def __init__(self, collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color):
        self.mass = mass
        self.color = color

        self.Pos = Vector(coords_tuple[0], coords_tuple[1])
        self.Vel = Vector(vel_tuple[0], vel_tuple[1])
        self.Acc = Vector(acc_tuple[0], acc_tuple[1])

        self.theta = theta
        self.omega = omega
        self.alpha = alpha

        self.F_move = Vector(0, 0)
        self.Fg = Vector(0, 0)
        self.F_g = Vector(0, 0 * self.mass * -25000)
        self.F_external = Vector(0, 0)
        self.torque = 0
        
        self.collision = collision
        self.gravity = gravity

        self.inside = False
        Objects.object_list.append(self)

    @staticmethod
    def num_obj():
        return Objects.number_of_objects

    def delete(self):
        del self


class Circle(Objects):
    def __init__(self, collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color, radius):
        super().__init__(collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color)
        self.radius = radius
        self.moment_inertia = (self.mass * (self.radius ** 2)) / 2


class Polygon(Objects):
    def __init__(self, collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color, n, radius):
        super().__init__(collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color)
        self.n = n
        self.delta = 2*pi/n
        self.radius = radius
        self.points = []

        if n >= 3:
            for i in range(1, ceil(n/2)):
                point = (self.radius * cos(pi/2 + i * self.delta), self.radius * sin(pi/2 + i * self.delta))
                self.points.append(point)

            # Symmetry
            points_reversed = reversed(self.points)
            for p in points_reversed:
                self.points.append((-p[0], p[1]))

            # Points on Y axis
            self.points.insert(0, (0, self.radius))
            if (n % 2) == 0:
                self.points.insert(floor(n/2), (0, -self.radius))

        else:
            print("number of sides of a polygon cannot be less than 3, object was not created")
            self.points = [(10000, 10000), (10000, 10000), (10000, 10000)]


class Rectangle(Objects):
    def __init__(self, collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color, width, height):
        super().__init__(collision, gravity, mass, coords_tuple, vel_tuple, acc_tuple, theta, omega, alpha, color)
        self.width = width
        self.height = height
        self.moment_inertia = (self.mass * (self.width ** 2 + self.height ** 2)) / 12
