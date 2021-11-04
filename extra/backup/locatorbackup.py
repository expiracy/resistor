import cv2
import matplotlib.pyplot as plt
import numpy as np

from detection.Annotation import Annotation
from detection.Graph import Graph
from detection.Greyscale import Greyscale
from detection.Line import Line
from detection.MergeSort import MergeSort


class ResistorLocator:

    def __init__(self, image):
        self.image = image

    def find_biggest_contour(self, contours):
        contour_areas = []
        area_for_contour = {}

        for contour in contours:
            contour_area = cv2.contourArea(contour)
            contour_areas.append(contour_area)
            area_for_contour[contour_area] = contour

        contour_areas = [cv2.contourArea(contour) for contour in contours]

        sorted_contour_areas = MergeSort().sort(contour_areas)

        # Biggest contour is most likely the resistor body.

        biggest_contour_area = sorted_contour_areas[len(sorted_contour_areas) - 1]

        return area_for_contour[biggest_contour_area]

    def find_erode_iterations(self, image, contours):
        image = Greyscale(image.image)

        biggest_initial_contour = self.find_biggest_contour(contours)

        biggest_initial_contour_area = cv2.contourArea(biggest_initial_contour)

        squared_contour_areas = [biggest_initial_contour_area ** 2]
        empty_image = False

        while not empty_image:

            eroded_image = image.erode(1)

            if eroded_image.count_non_zero_pixels() != 0:

                #eroded_image.show()

                contours, _ = eroded_image.find_contours()
                biggest_contour = self.find_biggest_contour(contours)
                contour_area = cv2.contourArea(biggest_contour)

                squared_contour_areas.append(contour_area ** 2)

            else:
                empty_image = True

        Graph().graph_x_against_y(range(0, len(squared_contour_areas)), squared_contour_areas, 'Erode Iteration', 'Squared Contour Area', 'Squared Contour Area Vs Erode Iteration')

        spine_line = Line([0, squared_contour_areas[0]], [len(squared_contour_areas) - 1, squared_contour_areas[len(squared_contour_areas) - 1]])

        y_spine_intersections = []

        for x in range(0, len(squared_contour_areas)):
            y = spine_line.solve_for_y(x)
            #plt.scatter(x, y)

            y_spine_intersections.append(y)

        spine_line_tangent = spine_line.tangent()

        for y in squared_contour_areas:
            x = spine_line_tangent.solve_for_x(y)
            print(x)
            #plt.scatter(x, y)


        print(y_spine_intersections)

        x = range(0, len(squared_contour_areas))
        y = squared_contour_areas

        plt.plot(x, y)
        plt.scatter(x, y)

        x_spine = [x[0], x[len(x) - 1]]
        y_spine = [y[0], y[len(y) - 1]]

        plt.plot(x_spine, y_spine, label="spine")

        # function to show the plot
        plt.show()

        spine_line_tangent = spine_line.tangent()


        differences = np.diff(squared_contour_areas)
        differences_of_differences = np.diff(differences)

        return np.where(differences_of_differences == max(differences_of_differences))[0][0] + 3

    def find_resistor_contour(self):
        greyscale_image = Greyscale(self.image.image, 'BGR')

        monochrome_image = greyscale_image.monochrome(inverted=True, block_size=51, C=21)

        contours, _ = monochrome_image.find_contours()

        # Fill in the holes in the resistor area so we can safely erode the image later
        filled_image = Annotation(monochrome_image.image).draw_contours(contours)

        # Erode the wires away - the ksize needs to be bigger than wires and smaller than resistor body

        filled_image = Greyscale(filled_image.image)

        erode_iterations = self.find_erode_iterations(filled_image.clone(), contours)

        eroded_image = filled_image.erode(erode_iterations + 1)

        #eroded_image.show()

        # Now the biggest contour should only be the resistor body

        contours, _ = eroded_image.find_contours()

        resistor_body_contour = self.find_biggest_contour(contours)

        return resistor_body_contour

    # From https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
    def extract_resistor(self, rectangle):
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)

        # get width and height of the detected rectangle
        width = int(rectangle[1][0])
        height = int(rectangle[1][1])

        src_pts = box.astype("float32")

        # coordinate of the points in box points after the rectangle has been
        # straightened
        dst_pts = np.array([[0, height - 1],
                            [0, 0],
                            [width - 1, 0],
                            [width - 1, height - 1]], dtype="float32")

        # the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # directly warp the rotated rectangle to get the straightened rectangle
        self.image = self.image.warp_perspective(matrix, width, height)

        if self.image.width() < self.image.height():
            self.image = self.image.rotate_90_clockwise()

        return self.image

    def locate(self):
        try:
            resistor_body_contour = self.find_resistor_contour()

            # This should  wrap a box with the correct orientation around the resistor body
            minimum_rectangle = cv2.minAreaRect(resistor_body_contour)

            resistor_image = self.extract_resistor(minimum_rectangle)

            return resistor_image

        except ValueError:
            print("Error with ResistorLocator.")