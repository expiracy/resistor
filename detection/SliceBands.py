import numpy as np
from sklearn.cluster import KMeans
import math

from detection.Resistor import Resistor


class SliceBands:
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

        x_list = []

        for bands_for_slice in self.slice_bands:
            slices_x_list.append([bands.bounding_rectangle.x for bands in bands_for_slice])
            slices_y_list.append([bands.bounding_rectangle.y for bands in bands_for_slice])
            slices_widths.append([bands.bounding_rectangle.width for bands in bands_for_slice])
            slices_heights.append([bands.bounding_rectangle.height for bands in bands_for_slice])
            slices_colours.append([bands.colour for bands in bands_for_slice])

            for band in bands_for_slice:
                x_list.append(band.bounding_rectangle.x)

        return slices_x_list, x_list, slices_x_list, slices_x_list, slices_x_list, slices_x_list

    def find_cluster(self, data):
        np_data = np.array(data)

        reshaped_data = np_data.reshape(len(np_data), 1)

        #FIX LATER

        max_list_length = len(max(self.bands_attributes()[0], key=len))


        clusters = KMeans(n_clusters=6).fit(reshaped_data)

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

                    if difference < mean_difference * 0.2:
                        slice_band.dupe = True
                        previous_band.dupe = True

                previous_band = slice_band

    def check_valid_slices(self):
        for slice_number in self.slice_bands:

            values = Resistor(slice_number).standard_values()


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

    def most_frequent_bands(self, possible_bands):
        try:
            resistor_bands = []

            for index in range(len(possible_bands[0])):
                band_colours = [bands[index] for bands in possible_bands]

                band_colour = max(set(band_colours), key=band_colours.count)

                resistor_bands.append(band_colour)

            print(resistor_bands)

        except:
            print("Error with input list.")

        return resistor_bands

    def find_bands(self, clusters):
        centers = [round(center[0], 10) for center in clusters.cluster_centers_]

        sorted_centers = sorted(centers)

        differences = np.diff(sorted_centers)

        mean_difference = np.mean(differences)

        previous_center = 0

        for center in sorted_centers:
            if (center - previous_center) < mean_difference:
                sorted_centers.remove(center)

            previous_center = center

        possible_bands = []

        for slice_number in self.slice_bands:

            slice_colours = []

            for slice_band in slice_number:
                if len(slice_number) == len(sorted_centers):

                    for center in sorted_centers:
                        if (center - (center * 0.2)) < slice_band.bounding_rectangle.x < (center + (center * 0.2)):
                            slice_colours.append(slice_band.colour)

                    possible_bands.append(slice_colours)

        return self.most_frequent_bands(possible_bands)

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

    def find_resistor_bands(self):
        self.remove_outliers()

        self.order_bands()

        self.identify_dupes()
        self.keep_biggest_dupe_band()

        self.order_bands()

        clusters = self.find_cluster(self.bands_attributes()[1])
        resistor_bands = self.find_bands(clusters)

        self.check_valid_slices()

        print("DONE\n\n\n")