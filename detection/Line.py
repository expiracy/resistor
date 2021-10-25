import numpy as np

class Line:
    def __init__(self, point_1, point_2):
        self.gradient = self.find_gradient(point_1, point_2)
        self.c = self.find_y_intercept(point_1)

    def find_gradient(self, point_1, point_2):
        try:
            dx = (point_1[0] - point_2[0])
            dy = (point_1[1] - point_2[1])

            gradient = dy / dx

            return gradient

        except ZeroDivisionError:
            print("Line is vertical.")
            return None

    def find_y_intercept(self, point):

        if self.gradient is not None:
            return point[1] - self.gradient * point[0]

        else:
            return None

    def solve_for_x(self, y):
        if self.gradient is not None and self.c is not None:
            return (y - self.c) / self.gradient

        else:
            print('Can not solve on a vertical line')

    def solve_for_y(self, x):
        if self.gradient is not None and self.c is not None:
            return float(self.gradient) * x + float(self.c)

        else:
            print('Can not solve on a vertical line')

    def tangent(self):
        self.gradient = -1 / self.gradient

        return self
