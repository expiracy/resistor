import numpy as np
from detection.KMeans import KMeans
import math

from detection.Resistor import Resistor


class SliceBandSelector:
    def __init__(self, slice_bands=None):
        self.slice_bands = slice_bands

    def order_bands(self, reverse=False):
        for slice_number in range(len(self.slice_bands)):
            self.slice_bands[slice_number] = sorted(self.slice_bands[slice_number],
                                                    key=lambda slice_band: slice_band.bounding_rectangle.x,
                                                    reverse=reverse)

    def bands_attributes(self):
        slices_x_list = []
        slices_y_list = []
        slices_widths = []
        slices_heights = []
        slices_colours = []

        for bands_for_slice in self.slice_bands:
            slices_x_list.append([bands.bounding_rectangle.x for bands in bands_for_slice])
            slices_y_list.append([bands.bounding_rectangle.y for bands in bands_for_slice])
            slices_widths.append([bands.bounding_rectangle.width for bands in bands_for_slice])
            slices_heights.append([bands.bounding_rectangle.height for bands in bands_for_slice])
            slices_colours.append([bands.colour for bands in bands_for_slice])

        return slices_x_list, slices_x_list, slices_x_list, slices_x_list, slices_x_list

    def find_x_cluster(self, x_list):
        x_y_list = [[x, 0] for x in x_list]
        np_x_y_list = np.array(x_y_list)

        optimal_k = KMeans().find_optimal_k(np_x_y_list)

        if optimal_k:
            clusters = KMeans(optimal_k).fit(np_x_y_list)

        else:
            max_list_length = len(max(self.bands_attributes()[0], key=len))

            if max_list_length > 6:
                max_list_length = 6

            clusters = KMeans(max_list_length).fit(np_x_y_list)

        return clusters

    def identify_dupes(self):
        # if 2 x coordinates are less than 0.4 x the mean difference away from each other, assume it is a duplicate band
        for slice_number in self.slice_bands[:]:

            x_list = [slice_band.bounding_rectangle.x for slice_band in slice_number]

            if len(x_list) > 1:

                differences = np.diff(x_list)
                mean_difference = np.mean(differences)

            else:
                mean_difference = 0

            previous_band = None

            for slice_band in slice_number[:]:

                if previous_band:
                    difference = slice_band.bounding_rectangle.x - previous_band.bounding_rectangle.x

                    if difference < mean_difference * 0.3:
                        slice_band.dupe = True
                        previous_band.dupe = True

                previous_band = slice_band

    def keep_biggest_dupe_band(self):
        for slice_number in self.slice_bands:

            areas = [slice_band.bounding_rectangle.width * slice_band.bounding_rectangle.height
                     for slice_band in slice_number if slice_band.dupe is True]

            if areas:
                # I am assuming that the best colour match is the best band
                biggest_area = max(areas)
                biggest_area_index = areas.index(biggest_area)

                for slice_band in slice_number:
                    if slice_band.dupe is True:
                        if slice_number.index(slice_band) != biggest_area_index:
                            slice_number.remove(slice_band)

    def identify_possible_bands(self, sorted_centroids, deviation):
        possible_bands = []

        debug = []

        for slice_number in self.slice_bands:

            slice_colours = []

            if len(slice_number) == len(sorted_centroids):

                for slice_band in slice_number:

                    slice_band_x_list = [slice_band.bounding_rectangle.x] * len(sorted_centroids)

                    differences = np.subtract(sorted_centroids, slice_band_x_list)

                    abs_differences = [abs(difference) for difference in differences]

                    smallest_difference_index = abs_differences.index(min(abs_differences))

                    nearest_centroid = sorted_centroids[smallest_difference_index]

                    #print(f'COLOUR: {slice_band.colour}')
                    #print(f'data: {slice_band.bounding_rectangle.x}')
                    #print(f'UPPER: {nearest_centroid - (nearest_centroid * 0.25)} LOWER: {nearest_centroid + (nearest_centroid * 0.25)}')
                    #print(f'\n')

                    if (nearest_centroid - (nearest_centroid * deviation)) < slice_band.bounding_rectangle.x < (
                            nearest_centroid + (nearest_centroid * deviation)):
                        slice_colours.append(slice_band.colour)

                if len(slice_colours) == len(sorted_centroids):
                    possible_bands.append(slice_colours)

                    debug.append(slice_number)

        return possible_bands

    def remove_bands_in_bands(self):
        for slice_number_1 in self.slice_bands:
            for slice_number_2 in self.slice_bands:

                for slice_band_1 in slice_number_1:
                    for slice_band_2 in slice_number_2:

                        upper_range = slice_band_1.bounding_rectangle.x + (slice_band_1.bounding_rectangle.width * 0.9)
                        lower_range = slice_band_1.bounding_rectangle.x + (slice_band_1.bounding_rectangle.x * 0.1)

                        if lower_range < slice_band_2.bounding_rectangle.x < upper_range:
                            slice_number_2.remove(slice_band_2)

    def identify_clustered_bands(self, clusters):

        centroids = []

        for centroid_number, centroid in clusters.centroids.items():
            centroids.append(centroid[0])

        sorted_centroids = sorted(centroids)

        differences = np.diff(sorted_centroids)

        mean_difference = np.mean(differences)

        previous_centroid = 0

        for centroid in sorted_centroids:
            difference = centroid - previous_centroid

            if difference < (mean_difference * 0.4):
                sorted_centroids.remove(centroid)

            previous_centroid = centroid

        possible_bands = self.identify_possible_bands(sorted_centroids, 0.1)

        if len(possible_bands) < 10:

            deviation = 0.11

            while len(possible_bands) < 3 and deviation < 0.3:

                possible_bands = self.identify_possible_bands(sorted_centroids, deviation)

                deviation += 0.01

        if possible_bands:
            return possible_bands

        else:
            return None

    def remove_outliers(self):
        for slice_number in self.slice_bands:
            widths = [slice_band.bounding_rectangle.width for slice_band in slice_number]
            heights = [slice_band.bounding_rectangle.height for slice_band in slice_number]

            resistor_height = max(heights)
            mean_band_width = np.mean(widths)

            for slice_band in slice_number[:]:

                if slice_band.bounding_rectangle.height < (
                        resistor_height * 0.7) or slice_band.bounding_rectangle.width < (mean_band_width * 1):
                    slice_number_index = self.slice_bands.index(slice_number)
                    self.slice_bands[slice_number_index].remove(slice_band)

    def find_possible_bands(self):
        try:
            self.remove_outliers()

            self.order_bands()

            self.identify_dupes()
            self.keep_biggest_dupe_band()

            self.remove_bands_in_bands()

            self.order_bands()

            x_list = []

            for slice_number in self.bands_attributes()[0]:
                for x in slice_number:
                    x_list.append(x)

            clusters = self.find_x_cluster(x_list)
            possible_bands = self.identify_clustered_bands(clusters)

            return possible_bands

        except:
            print("Error with SliceBandSelector.")

