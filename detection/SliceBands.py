import numpy as np
from sklearn.cluster import KMeans


class SliceBands:
    def __init__(self, slice_bands=None):
        self.slice_bands = slice_bands

    def order_bands(self, reverse=False):

        for slice_number in range(len(self.slice_bands)):
            self.slice_bands[slice_number] = sorted(self.slice_bands[slice_number],
                                                    key=lambda slice_band: slice_band.bounding_rectangle.x,
                                                    reverse=reverse)

    def bands_attributes(self):

        x_list = []
        y_list = []
        widths = []
        heights = []
        colours = []

        for bands_for_slice in self.slice_bands:
            for bands in bands_for_slice:
                x_list.append(bands.bounding_rectangle.x)
                y_list.append(bands.bounding_rectangle.y)
                widths.append(bands.bounding_rectangle.width)
                heights.append(bands.bounding_rectangle.height)
                colours.append(bands.colour)

        return x_list, y_list, widths, heights, colours

    def k_means(self, array):

        array = np.reshape(array, (1, -1)).T

        mean = np.mean(array)

        print(mean)

        k_mean = KMeans(n_clusters=4)

        k_mean.fit(array)
        labels = k_mean.labels_
        var = k_mean.cluster_centers_

        print(var)
        print(labels)

    def remove_dupes(self):

        # if 2 x coordinates are less than 0.4 x the mean difference away from each other, assume it is a duplicate band
        for slice_number in self.slice_bands[:]:

            slice_number_index = self.slice_bands.index(slice_number)

            x_list = [slice_band.bounding_rectangle.x for slice_band in slice_number]
            differences = np.diff(x_list)
            mean_difference = np.mean(differences)

            previous_band = None

            for slice_band in slice_number[:]:

                if previous_band:
                    difference = slice_band.bounding_rectangle.x - previous_band.bounding_rectangle.x

                    if difference < mean_difference * 0.4:
                        slice_band.dupe = True
                        previous_band.dupe = True

                previous_band = slice_band

        for slice_number in self.slice_bands[:]:
            for slice_band in slice_number[:]:
                if slice_band.dupe is True:
                    slice_number.remove(slice_band)

    def remove_outliers(self):

        widths = self.bands_attributes()[2]
        heights = self.bands_attributes()[3]

        resistor_height = max(heights)
        mean_band_width = np.mean(widths)

        for slice_number in self.slice_bands:
            for slice_band in slice_number[:]:

                if slice_band.bounding_rectangle.height < (
                        resistor_height * 0.7) or slice_band.bounding_rectangle.width < (mean_band_width * 1):
                    slice_number_index = self.slice_bands.index(slice_number)
                    self.slice_bands[slice_number_index].remove(slice_band)

    def find_resistor_bands(self):
        self.remove_outliers()
        self.order_bands()
        self.remove_dupes()

        print("dsjhidhakd")
