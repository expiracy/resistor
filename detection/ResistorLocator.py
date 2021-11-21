import cv2
import numpy as np

from detection.Annotation import Annotation
from detection.Contours import Contours
from detection.Greyscale import Greyscale
from detection.Line import Line


# Initiates with an image and contains various operations that aid with the location of a resistor.
class ResistorLocator:
    def __init__(self, image):
        self.image = image

    # Finding the amount of erosion needed to remove the resistor wires.
    def find_erode_iterations(self, image, contours):
        try:
            image = Greyscale(image.image)

            biggest_initial_contour = Contours(contours).find_biggest()

            biggest_initial_contour_area = cv2.contourArea(biggest_initial_contour)

            squared_contour_areas = [biggest_initial_contour_area ** 2]

            empty_image = False

            while not empty_image:

                eroded_image = image.erode(1)

                if eroded_image.count_non_zero_pixels() != 0:

                    # eroded_image.show()

                    contours, _ = eroded_image.find_contours()
                    biggest_contour = Contours(contours).find_biggest()

                    contour_area = cv2.contourArea(biggest_contour)
                    squared_contour_areas.append(contour_area ** 2)

                else:
                    empty_image = True

            # Graph().graph_x_against_y(range(0, len(squared_contour_areas)), squared_contour_areas, 'Erode Iteration', 'Squared Contour Area', 'Squared Contour Area Vs Erode Iteration')

            points = []

            for x_index in range(len(squared_contour_areas)):
                points.append([x_index, squared_contour_areas[x_index]])

            knee = Line().find_knee(points)

            safe_knee = knee + 5

            return safe_knee

        except Exception as error:
            raise Exception(f'Error trying to find erode iterations, {error}')

    # Finding the contour of the resistor body.
    def find_resistor_contour(self):
        try:
            greyscale_image = Greyscale(self.image.image, 'BGR')

            monochrome_image = greyscale_image.monochrome(inverted=True, block_size=151, C=21)

            contours, _ = monochrome_image.find_contours()

            # Fill in the holes in the resistor area so we can safely erode the image later
            filled_image = Annotation(monochrome_image.image).draw_contours(contours)

            # Erode the wires away - the number of iterations needs to be bigger than wires and smaller than resistor body.
            filled_image = Greyscale(filled_image.image)

            erode_iterations = self.find_erode_iterations(filled_image.clone(), contours)

            eroded_image = filled_image.erode(erode_iterations)

            # eroded_image.show()

            # The biggest contour should only be the resistor body
            contours, _ = eroded_image.find_contours()

            resistor_body_contour = Contours(contours).find_biggest()

            return resistor_body_contour

        except Exception as error:
            raise Exception(f'Error trying to find resistor contour, {error}')

    # Extracts the resistor from a rectangle
    def extract_resistor(self, resistor_body_contour):
        try:
            resistor_rectangle = cv2.minAreaRect(resistor_body_contour)

            box = cv2.boxPoints(resistor_rectangle)
            box = np.int0(box)

            # Get width and height of the detected resistor_rectangle.
            width = int(resistor_rectangle[1][0])
            height = int(resistor_rectangle[1][1])

            source_points = box.astype('float32')

            # Coordinate of the points in box points after the resistor_rectangle has been straightened.
            destination_points = np.array([[0, height - 1],
                                           [0, 0],
                                           [width - 1, 0],
                                           [width - 1, height - 1]], dtype='float32')

            # The perspective transformation.
            matrix = cv2.getPerspectiveTransform(source_points, destination_points)

            # directly warp the rotated resistor_rectangle to get the straightened resistor_rectangle
            self.image = self.image.warp_perspective(matrix, width, height)

            if self.image.width() < self.image.height():
                self.image = self.image.rotate_90_clockwise()

            return self.image

        except Exception as error:
            raise Exception(f'Error trying to extract resistor, {error}')

    # Extracts the image of the resistor body from a resistor body contour.
    def locate(self):
        try:
            resistor_body_contour = self.find_resistor_contour()

            resistor_image = self.extract_resistor(resistor_body_contour)

            return resistor_image

        except Exception as error:
            raise Exception(f'Error locating resistor in image, {error}')
