import cv2
import uuid
import os
import numpy as np

class Image:

    def __init__(self, image=None):
        self.image = image

    def clone(self):
        return Image(self.image)

    def load(self, location):

        self.image = cv2.imread(location)

        return self

    def width(self):

        return self.image.shape[1]

    def height(self):

        return self.image.shape[0]

    def resize(self, width, height):

        self.image = cv2.resize(self.image, (width, height))

        return self

    def region(self, x, y, width, height):

        self.image = self.image[y:y + height, x:x + width]

        return self

    def show(self):

        cv2.imshow("Image", self.image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            color = hsv_image[y][x]

            print(color)

    def rotate(self, angle, center=None, scale=1.0):
        height = self.height()
        width = self.width()

        if center is None:
            center = (width / 2, height / 2)

        matrix = cv2.getRotationMatrix2D(center, angle, scale)

        abs_cos = abs(matrix[0, 0])
        abs_sin = abs(matrix[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        matrix[0, 2] += bound_w / 2 - center[0]
        matrix[1, 2] += bound_h / 2 - center[1]

        self.image = cv2.warpAffine(self.image, matrix, (bound_w, bound_h))

        return self

    def save(self):
        filename = str(uuid.uuid1().int)

        absolute_file_path = f'{os.path.abspath(os.curdir)}\\resistorImages\\{filename}.jpg'

        if not cv2.imwrite(f'{absolute_file_path}', self.image):
            raise Exception("Could not write image.")

        return absolute_file_path

    def warp_perspective(self, matrix, width, height):
        self.image = cv2.warpPerspective(self.image, matrix, (width, height))

        return self

    def erode(self):
        element = cv2.getStructuringElement(cv2.MORPH_ERODE, (9, 9), (3, 3))
        self.image = cv2.erode(self.image, element, iterations=2)

        return self






