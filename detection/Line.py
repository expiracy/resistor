import numpy as np

class Line:
    def __init__(self):
        self.gradient = None
        self.constant = None

    # Make a line from 2 points.
    def from_points(self, start_point, end_point):

        line = Line()

        line.gradient = self.find_gradient(start_point, end_point)
        line.constant = start_point[1] - line.gradient * start_point[0]

        return line

    # Make a line from a point and a gradient.
    def from_gradient(self, gradient, start_point):

        line = Line()

        line.gradient = gradient
        line.constant = start_point[1] - line.gradient * start_point[0]

        return line

    # Find the gradient of a line from 2 points.
    def find_gradient(self, start_point, end_point):
        try:
            dx = (end_point[0] - start_point[0])
            dy = (end_point[1] - start_point[1])

            gradient = dy / dx

            return gradient

        except ZeroDivisionError:
            print('Line is vertical.')
            return None

    # Find the constant value of the line.
    def find_constant(self, point):

        if self.gradient is not None:
            return point[1] - self.gradient * point[0]

        else:
            return None

    # Solve the line for the x value from a y value.
    def solve_for_x(self, y):
        if self.gradient is not None and self.constant is not None:
            return (y - self.constant) / self.gradient

        else:
            print('Can not solve on a vertical or horizontal line.')

    # Solve the line for the y value from an x value.
    def solve_for_y(self, x):
        if self.gradient is not None and self.constant is not None:
            return float(self.gradient) * x + float(self.constant)

        else:
            print('Can not solve on a vertical or horizontal line.')

    # Returns the normal gradient.
    def normal(self):
        try:
            return -1 / self.gradient

        except Exception as E:
            print('Line has no gradient.')
            print(E)

    # Finds the intersection of 2 lines.
    def find_intersection(self, line_2):
        try:
            x = (line_2.constant - self.constant) / (self.gradient - line_2.gradient)
            y = self.solve_for_y(x)

            intersection = [x, y]

            return intersection

        except Exception as E:
            print('Error finding intersection.')
            print(E)

    # Finds the length of 2 lines between 2 points.
    def length(self, point_1, point_2):
        try:
            dx_squared = (point_1[0] - point_2[0]) ** 2
            dy_squared = (point_1[1] - point_2[1]) ** 2

            distance = np.sqrt(dx_squared + dy_squared)

            return distance

        except Exception as E:
            print('Error finding line length.')
            print(E)

    # Finds the knee of data.
    def find_knee(self, points):
        try:
            start_point = points[0]
            end_point = points[len(points) - 1]

            spine = self.from_points(start_point, end_point)

            intersection_distances = []

            for current_point in points:
                current_line = self.from_gradient(spine.normal(), current_point)

                intersection = current_line.find_intersection(spine)

                distance = current_line.length(intersection, current_point)

                intersection_distances.append(distance)

            knee = intersection_distances.index(max(intersection_distances))

            return knee

        except Exception as E:
            print('Error finding knee.')
            print(E)
