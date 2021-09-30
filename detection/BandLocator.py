import cv2
import numpy
import numpy as np

import os
import glob

from detection.HSV import HSV

from detection.Colours import Colours
from detection.Image import Image
from detection.ResistorBand import ResistorBand
from detection.Resistor import Resistor
from detection.BoundingRectangle import BoundingRectangle
from detection.Greyscale import Greyscale
from detection.BGR import BGR
from detection.SliceBands import SliceBands
from detection.SliceBand import SliceBand
from detection.Glare import Glare
from detection.Annotation import Annotation

class BandLocator:

    def __init__(self, image):
        self.image = image

    def remove_outlier_contours(self, contours):

        bounding_rectangles = []

        for contour in contours:
            bounding_rectangle = BoundingRectangle(contour)

            bounding_rectangles.append(bounding_rectangle)

        areas = [bounding_rectangle.width * bounding_rectangle.height for bounding_rectangle in bounding_rectangles]

        mean = np.mean(areas)

        lower_bound = mean - (mean * 0.6)

        # write about different outlier algorithms tried

        for index in range(len(areas))[:]:
            if areas[index] < lower_bound:
                contours.remove(contours[index])

        return contours

    def bands(self, image_slice):

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD',
                   'SILVER']

        bands = []

        for colour in colours:

            hsv_ranges = Colours().lookup_hsv_range(colour)

            hsv_image = HSV(image_slice.image, 'BGR')
            colour_mask = hsv_image.mask(hsv_ranges)

            greyscale_mask_image = Greyscale(colour_mask, 'HSV')

            non_zero_pixels = greyscale_mask_image.count_non_zero_pixels()

            band_contours = None

            if non_zero_pixels != 0:
                band_contours, _ = greyscale_mask_image.find_contours()

            if band_contours is not None:

                print(colour)

                #greyscale_mask_image.show()

                for contour in band_contours:
                    bounding_rectangles = BoundingRectangle(contour)

                    band = SliceBand(colour, bounding_rectangles)

                    bands.append(band)

        return bands

    def remove_glare_from_image(self, glare_mask):
        self.image.mask(glare_mask.image)

        contours, _ = Greyscale(self.image.image).find_contours()

        largest_contour = max(contours, key=cv2.contourArea)

        bounding_rectangle = BoundingRectangle(largest_contour)

        #annotated_image = Annotation(self.image.image).draw_rectangle(bounding_rectangle.x, bounding_rectangle.y, bounding_rectangle.width, bounding_rectangle.height)
        #annotated_image.show()

        self.image = self.image.region(bounding_rectangle.x, bounding_rectangle.y, bounding_rectangle.width, bounding_rectangle.height)

        return self

    def locate(self):

        self.image = self.image.resize(self.image.width(), self.image.height() * 10)

        glare_mask = Glare(self.image).locate()

        self.remove_glare_from_image(glare_mask)

        self.image = self.image.resize(self.image.width(), self.image.height() * 5)

        self.image = BGR(self.image.image).blur(1, round(self.image.height() * 0.5))

        self.image.show()

        image_slices = self.image.slices(round(self.image.height() * 0.05))

        slice_bands = []

        for image_slice in image_slices:
            bands_for_slice = self.bands(image_slice)

            image_slice.show()

            slice_bands.append(bands_for_slice)

        SliceBands(slice_bands).find_resistor_bands()

        # resistor = Resistor(bands_for_slice).main()

        # print(resistor.colours())


if __name__ == "__main__":
    directory = os.path.abspath(os.curdir)

    folder = f'{directory}\\resistorImages'

    for filename in os.listdir(folder):
        if filename.endswith('jpg'):
            resistor_image = cv2.imread(f'{folder}\\{filename}')
            resistor_image = Image(resistor_image)

            BandLocator(resistor_image).locate()
