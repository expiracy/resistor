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
    def __init__(self, image):
        self.image = image

    def locate(self):

        self.image.show()

        canny_image = self.image.blur(6, 6).greyscale().canny(150, 150)


        contours, _ = canny_image.contours()

        cropped_image = self.focus_image(contours, image)

        monochrome_image = cropped_image.blur(round(cropped_image.width() * 0.07), round(cropped_image.height() * 0.07)).greyscale().monochrome()
        monochrome_image.show()
        
        contours, _ = monochrome_image.contours()


        if len(contours) > 0:
            cnt = contours[len(contours) - 1]
            contours_image = cv2.drawContours(cropped_image.image, [cnt], 0, (0, 255, 0), 3)


        cv2.imshow("pog", contours_image)

        #canny_image = Image(cropped_image).greyscale().canny()

        x_centres, y_centres = self.find_cluster(contours)


        for k in range(len(x_centres)):
            x = int(x_centres[k][0])
            y = int(y_centres[k][0])
            cropped_image.draw_circle(x, y)

        cropped_image.show()


    def get_contour_coordinates(self, contours):
        x_list = []
        y_list = []

        for contour in contours:
            for index in contour:
                for type in index:
                    x_list.append(type[0])
                    y_list.append(type[1])

        return x_list, y_list

    def find_cluster(self, data):

        '''
        for coordinate in data:
            for x1, y1, x2, y2 in coordinate:

                x.append(x1)
                x.append(x2)

                y.append(y1)
                y.append(y2)
                
        '''

        x_list, y_list = self.get_contour_coordinates(data)

        X = numpy.float32(x_list)
        Y = numpy.float32(y_list)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)
        K = 100

        x_ret, x_label, x_centre = cv2.kmeans(X, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        y_ret, y_label, y_centre = cv2.kmeans(Y, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        return x_centre, y_centre

    def remove_outliers(self, data):
        std = numpy.std(data)
        mean = numpy.mean(data)

        upper = mean + (3 * std)
        lower = mean - (3 * std)

        for item in data:
            if item > upper or item < lower:
                data.remove(item)

        return data

    def focus_image(self, contours, image):

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

        width = largest_x - smallest_x
        height = largest_y - smallest_y

        cropped_image = image.region(smallest_x - round(image.width() * 0.025), smallest_y - round(image.width() * 0.025), width + round(image.width() * 0.05), height + round(image.width() * 0.05))

        #cropped_image.show()

        #cropped_image = numpy.array(cropped_image)

        return cropped_image


        #draw box round resistor using contours

    def find_widest_part(self):
        pass


if __name__ == "__main__":

    os.chdir("../..")

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
            cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), 
                         (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
            #cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

        cv2.imshow('Contours', drawing)

        cv2.waitKey(-1)
        
        '''

    image = Image().load(file_name)

    resistor_locator = ResistorLocator(image)

    resistor_locator.locate()
