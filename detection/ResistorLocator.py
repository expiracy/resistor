"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import os
import cv2
from Image import Image
import numpy
import glob
import random

class ResistorLocator:
    def __init__(self, image_file):
        self.image_file = image_file

    def locate(self):
        image = Image().load(self.image_file)
        image2 = Image().load(self.image_file)

        canny_image = Image(image.image).blur().greyscale().canny()

        contours = canny_image.contours()

        #canny_image = Image(image.image).blur().show()

       # canny_image.show()

        #contours = canny_image.contours(image.image)

        hough_lines_image, lines = image.hough_lines(canny_image.image)

        x_centres, y_centres = self.find_cluster(lines)

        self.bounding_box(contours, image)



        for k in range(len(x_centres)):
            x = int(x_centres[k][0])
            y = int(y_centres[k][0])
            image.draw_circle(x, y)


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

    def bounding_box(self, contours, image):

        x_list = []
        y_list = []

        for k in contours:
            for i in k:
                for j in i:
                    x_list.append(j[0])
                    y_list.append(j[1])

        x_list.sort()
        y_list.sort()

        largest_x = x_list[-1]
        smallest_x = x_list[0]

        largest_y = y_list[-1]
        smallest_y = y_list[0]

        image.draw_circle(largest_x, largest_y)
        image.draw_circle(largest_x, smallest_y)
        image.draw_circle(smallest_x, largest_y)
        image.draw_circle(smallest_x, smallest_y)

        image.show()

        #draw box round resistor using contours


if __name__ == "__main__":

    os.chdir("..")

    directory = os.path.abspath(os.curdir)

    file_name = f'{directory}\\images\\0.25_normal_IMG_3048.JPG'

    for file_name in glob.glob(directory + '\\images\\' + '*.jpg'):
        pass

        '''
        image = cv2.imread(file_name)

        canny = cv2.Canny(image, 100, 200, apertureSize=3)

        _, contours = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        centers = [None] * len(contours)
        radius = [None] * len(contours)
        for i, c in enumerate(contours):
            #contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            #centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

        drawing = numpy.zeros((canny.shape[0], canny.shape[1], 3), dtype=numpy.uint8)

        for i in range(len(contours)):
            color = (random .randint(0, 256), random .randint(0, 256), random.randint(0, 256))
            #cv2.drawContours(drawing, contours_poly, i, color)
            cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
                         (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
            #cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

        cv2.imshow('Contours', drawing)

        cv2.waitKey(-1)
        
        '''

    resistor_locator = ResistorLocator(file_name)

    resistor_locator.locate()
