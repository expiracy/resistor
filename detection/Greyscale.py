import cv2
import numpy as np

from detection.Image2 import Image2
from detection.BGR import BGR

class Greyscale(Image2):
    def __init__(self, image):
        greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        super().__init__(greyscale)

    def canny(self, threshold_1=50, threshold_2=50, aperture_size=3):
        self.image = cv2.Canny(self.image, threshold_1, threshold_2, aperture_size)

        return self

    def find_hough_lines(self, image, threshold=1, min_line_length=1, max_line_gap=1):
        lines = cv2.HoughLinesP(image, 100, np.pi / 180, threshold, min_line_length, max_line_gap)

        return lines

    def contours(self):
        contours, hierarchy = cv2.findContours(self.image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        return contours, hierarchy

    def count_non_zero_pixels(self):
        return cv2.countNonZero(self.image)

    def monochrome(self, inverted=False, block_size=51, C=21):
        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        self.image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding, block_size, C)

        return self

if __name__ == '__main__':
    image = Image2().load('C:\\Users\\expiracy\\PycharmProjects\\resistor\\images\\BROWN BLACK BROWN GOLD.JPG')

    image.height()

    test = Greyscale(image.image)
    test.save()

    blurred = BGR(test.image).greyscale_to_bgr().blur().show()
