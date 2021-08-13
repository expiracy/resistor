"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import os
import cv2
from Image import Image

class ResistorLocator:
    def __init__(self, image_file):
        self.image_file = image_file

    def locate(self):
        image = Image().load(self.image_file)

        greyscale = Image(image.image).apply_greyscale()
        canny = Image(greyscale.image).apply_canny()
        image.apply_kmeans().show()
        #hough_lines, lines = image.apply_hough_lines(canny.image)

if __name__ == "__main__":
    file_name = "0.25_normal_IMG_3048.jpg"

    os.chdir("..")

    image_file = f"{os.path.abspath(os.curdir)}\\images\\{file_name}"

    resistor_locator = ResistorLocator(image_file)

    resistor_locator.locate()
