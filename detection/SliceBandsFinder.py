import numpy as np

from detection.BGR import BGR
from detection.BoundingRectangle import BoundingRectangle
from detection.Colour import Colour
from detection.GlareRemover import GlareRemover
from detection.Greyscale import Greyscale
from detection.HSV import HSV
from detection.HSVRanges import HSVRanges
from detection.SliceBand import SliceBand
from detection.SliceBands import SliceBands


# Initiates with an image, slices the image and is responsible for finding the slice bands of each slice.
class SliceBandsFinder:
    def __init__(self, image):
        self.image = image
        self.slice_bands = SliceBands()

    # Check if the band is right at the edge of the image.
    def check_if_edge_band(self, bounding_rectangle):
        try:
            image_width = self.image.width()

            if bounding_rectangle.x == 0 or bounding_rectangle.x == image_width:
                return True

            else:
                return False

        except Exception as error:
            raise Exception(f'Error checking edge band, bounding rectangle is None, {error}')

    # Returns a mask for the specified colour on an image slice.
    def band_mask(self, colour, image_slice):
        try:
            hsv_ranges = HSVRanges().for_colour(colour)

            hsv_image = HSV(image_slice.image, 'BGR')

            colour_mask = hsv_image.mask(hsv_ranges)

            greyscale_mask_image = Greyscale(colour_mask, 'HSV')

            return greyscale_mask_image

        except Exception as error:
            raise Exception(f'Error masking band, {error}')

    # Finds the bands.
    def find_bands(self, image_slice, original_image_slice):
        try:
            for colour in Colour:

                greyscale_mask_image = self.band_mask(colour, image_slice)

                non_zero_pixels = greyscale_mask_image.count_non_zero_pixels()

                band_contours = None

                if non_zero_pixels != 0:
                    band_contours, _ = greyscale_mask_image.find_contours()

                if band_contours is not None:

                    for contour in band_contours:
                        bounding_rectangle = BoundingRectangle(contour)

                        edge_band = False

                        if colour == Colour.WHITE or colour == Colour.GREY:
                            edge_band = self.check_if_edge_band(bounding_rectangle)

                        if not edge_band:
                            hsv_variance = self.get_region_hsv_variance(original_image_slice, bounding_rectangle)

                            slice_band = SliceBand(colour, bounding_rectangle, hsv_variance)

                            self.slice_bands.add_band(slice_band)

            return self

        except Exception as error:
            raise Exception(f'Error trying to find bands for image slice, {error}')

    # Calculating the variance of a list of values
    def calculate_variance(self, values):
        try:
            number_of_values = len(values)

            values_sum = np.sum(values)
            mean = values_sum / number_of_values

            squared_value_mean_differences = [(value - mean) ** 2 for value in values]

            sum_value_mean_differences = sum(squared_value_mean_differences)

            variance = sum_value_mean_differences / number_of_values

            return variance

        except Exception as error:
            raise Exception(f'Error to calculate variance: {error}')

    def get_region_hsv_variance(self, image_slice, bounding_rectangle):
        try:

            slice_band_image = image_slice.clone().region(bounding_rectangle.x,
                                                          bounding_rectangle.y,
                                                          bounding_rectangle.width,
                                                          bounding_rectangle.height)

            h_values = []
            s_values = []
            v_values = []

            for x in slice_band_image.image:
                for y in x:
                    h_values.append(y[0])
                    s_values.append(y[1])
                    v_values.append(y[2])

            h_variance, s_variance, v_variance = self.calculate_variance(h_values), self.calculate_variance(
                s_values), self.calculate_variance(v_values)

            squared_h_variance, squared_s_variance, squared_v_variance = h_variance ** 2, s_variance ** 2, v_variance ** 2

            squared_hsv_variances = [squared_h_variance, squared_s_variance, squared_v_variance]

            sum_of_squared_hsv_variances = np.sum(squared_hsv_variances)

            hsv_variance = np.sqrt(sum_of_squared_hsv_variances)

            return hsv_variance

        except Exception as error:
            print(f'get_region_hsv_variance(), {error}')

    # Finds all the bands for all slices.
    def find_all_bands(self):
        try:
            self.image = self.image.resize(self.image.width(), self.image.height() * 20)

            self.image = GlareRemover(self.image).main()

            self.image = self.image.resize(self.image.width(), self.image.height() * 5)

            self.image = self.image.region(0, round(self.image.height() * 0.1), self.image.width(),
                                           round(self.image.height() * 0.8))

            blurred_image = BGR(self.image.image).blur(2, round(self.image.height() * 0.5))

            # blurred_image.show()

            image_slices = blurred_image.create_slices(round(blurred_image.height() * 0.05))

            original_image = self.image.clone()

            original_image_slices = original_image.create_slices(round(original_image.height() * 0.05))

            for index in range(len(image_slices)):
                self.find_bands(image_slices[index], original_image_slices[index])

            return self.slice_bands

        except Exception as error:
            raise Exception(f'Error finding slice bands, {error}')
