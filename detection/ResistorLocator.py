"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import os
import cv2
from Image import Image
from matplotlib import pyplot
import numpy
import glob

class ResistorLocator:
    def __init__(self, image_file):
        self.image_file = image_file

    def locate(self):
        image = Image().load(self.image_file)

        canny_image = Image(image.image).greyscale().canny()

        canny_image.show()

        #contours = canny_image.contours(image.image)

        hough_lines_image, lines = image.hough_lines(canny_image.image)

        x_centres, y_centres = self.find_cluster(lines)



        for k in range(len(x_centres)):
            image.draw_circle(x_centres[k][0], y_centres[k][0])


        image.show()

    def find_cluster(self, coordinates):

        x = []
        y = []

        for coordinate in coordinates:
            for x1, y1, x2, y2 in coordinate:

                x.append(x1)
                x.append(x2)

                y.append(y1)
                y.append(y2)

        X = numpy.float32(x)
        Y = numpy.float32(y)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)
        K = 1

        x_ret, x_label, x_centre = cv2.kmeans(X, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        y_ret, y_label, y_centre = cv2.kmeans(Y, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        return x_centre, y_centre



if __name__ == "__main__":

    os.chdir("..")

    directory = os.path.abspath(os.curdir)

    for file_name in glob.glob(directory + '\\images\\' + '*.jpg'):

        resistor_locator = ResistorLocator(file_name)

        resistor_locator.locate()
