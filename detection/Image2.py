import cv2
import uuid
import os
import numpy as np

from detection.Annotation import Annotation

class Image2:
    def __init__(self, image=None):
        self.image = image

    def clone(self):
        return Image2(self.image)

    def load(self, location):

        self.image = cv2.imread(location)

        return self

    def width(self):

        return np.size(self.image, 1)

    def height(self):

        return np.size(self.image, 0)

    def resize(self, width, height):

        return cv2.resize(self.image, (width, height))

    def region(self, x, y, width, height):

        return self.image[y:y + height, x:x + width]

    def show(self):

        cv2.imshow("Image", self.image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            color = hsv_image[y][x]

            print(color)

    def save(self):

        filename = str(uuid.uuid1().int)

        absolute_file_path = f'{os.path.abspath(os.curdir)}\\resistorImages\\{filename}.jpg'

        if not cv2.imwrite(f'{absolute_file_path}', self.image):
            raise Exception("Could not write image.")

        return absolute_file_path




