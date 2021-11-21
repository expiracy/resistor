import cv2
import numpy as np

from detection.Image import Image

'''
Initiates with an image and current image type (for conversion) and inherits from Image. Responsible for carrying out 
operations that work on HSV images.
'''


class HSV(Image):
    def __init__(self, image, type='HSV'):
        hsv = self.HSV_conversion(image, type)
        super().__init__(hsv)

    # Masking HSV ranges from an image.
    def mask(self, hsv_ranges):
        try:
            h, s, v = self.split()

            if hsv_ranges.h_range[0] > hsv_ranges.h_range[1]:
                h_range_1 = cv2.inRange(h, hsv_ranges.h_range[0], 180)
                h_range_2 = cv2.inRange(h, 0, hsv_ranges.h_range[1])

                h_range = cv2.bitwise_or(h_range_1, h_range_2)

            else:
                h_range = cv2.inRange(h, hsv_ranges.h_range[0], hsv_ranges.h_range[1])

            s_range = cv2.inRange(s, hsv_ranges.s_range[0], hsv_ranges.s_range[1])
            v_range = cv2.inRange(v, hsv_ranges.v_range[0], hsv_ranges.v_range[1])

            # Narrowing down the image to only show the HSV values of the desired range
            hs_mask = np.bitwise_and(h_range, s_range)
            hsv_mask = np.bitwise_and(hs_mask, v_range)

            return hsv_mask

        except:
            print(f'Error masking HSV ranges {hsv_ranges}')

    # Splitting and HSV image into its h, s and v components.
    def split(self):
        try:
            h, s, v = cv2.split(self.image)

            return h, s, v

        except Exception as error:
            raise Exception(f'Error splitting image into h, s, v components, {error}')

    # Conversion between types.
    def HSV_conversion(self, image, type):
        try:
            if type == 'BGR':
                return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            if type == 'HSV':
                return image

        except Exception as error:
            raise Exception(f'Error converting image from greyscale, {error}')
