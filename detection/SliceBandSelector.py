import numpy as np

from detection.KMeans import KMeans
from detection.MergeSort import MergeSort


class SliceBandSelector:
    def __init__(self, slice_bands=None):
        self.slice_bands = slice_bands

    # Ordering the bands based on the bounding box X coordinate.
    def order_bands(self, reverse=False):
        try:
            slices_x_lists = self.get_bands_attributes()[0]

            for index, slice_x_list in enumerate(slices_x_lists):
                sorted_slice_x_list = MergeSort().sort(slice_x_list, reverse=reverse)

                sorted_slice_bands = []

                for x in sorted_slice_x_list:
                    for slice_band in self.slice_bands[index]:

                        if slice_band.bounding_rectangle.x == x:

                            if slice_band not in sorted_slice_bands:
                                sorted_slice_bands.append(slice_band)

                self.slice_bands[index] = sorted_slice_bands

        except:
            raise Exception("Error while trying to order bands")

    # Returns list(s) of a certain attribute(s) from the slice bands.
    def get_bands_attributes(self):
        try:
            slices_x_lists = []
            slices_y_lists = []
            slices_widths = []
            slices_heights = []
            slices_colours = []

            for bands_for_slice in self.slice_bands:
                slices_x_lists.append([bands.bounding_rectangle.x for bands in bands_for_slice])
                slices_y_lists.append([bands.bounding_rectangle.y for bands in bands_for_slice])
                slices_widths.append([bands.bounding_rectangle.width for bands in bands_for_slice])
                slices_heights.append([bands.bounding_rectangle.height for bands in bands_for_slice])
                slices_colours.append([bands.colour for bands in bands_for_slice])

            return slices_x_lists, slices_y_lists, slices_widths, slices_heights, slices_colours

        except:
            raise Exception("Error trying to get band attributes")

    # Using K-means to find where there are clusters of X (locating the band).
    def find_x_cluster(self, x_list):
        try:
            x_y_z_list = np.array([[x, 0, 0] for x in x_list])

            k_means = KMeans()

            number_of_bands = k_means.find_optimal_number_of_clusters(x_y_z_list)

            if number_of_bands > 6 or None:
                number_of_bands = 4

            k_means.number_of_centroids = number_of_bands
            clusters = k_means.fit(x_y_z_list, k_means.initialize_centroids(x_y_z_list))

            return clusters, number_of_bands

        except:
            raise Exception("Error while trying to find x cluster")

    # Removing duplicate bands from the slice bands.
    def identify_dupes(self):
        try:
            # if 2 x coordinates are less than 0.3x the mean difference away from each other, assume it is a duplicate band
            for slice_number in self.slice_bands[:]:

                x_list = [slice_band.bounding_rectangle.x for slice_band in slice_number]

                if len(x_list) > 1:

                    mean_difference = self.find_mean_difference(x_list)

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

        except:
            raise Exception("Error while trying to identify dupe slice bands")

    # Select the biggest dupe band as it is more likely to be the correct band.
    def keep_biggest_dupe_band(self):
        try:
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

        except:
            raise Exception("Error while trying to keep biggest dupe band")

    # Finds the mean difference for a list.
    def find_mean_difference(self, list):
        try:
            differences = np.diff(list)
            mean_difference = np.mean(differences)

            return mean_difference

        except:
            raise Exception("Error while trying to find mean difference")

    # Identifying the slice bands that match up with the x centroids.
    def identify_possible_bands(self, sorted_centroids, deviation):
        try:
            possible_bands = {}

            for possible_band in range(len(sorted_centroids)):
                possible_bands[possible_band] = []

            mean_centroid_difference = self.find_mean_difference(sorted_centroids)

            for slice_number in self.slice_bands:
                for band_number, centroid in enumerate(sorted_centroids):
                    for slice_band in slice_number:
                        centroid_band_difference = abs(slice_band.bounding_rectangle.x - centroid)
                        if centroid_band_difference < mean_centroid_difference * deviation:
                            possible_bands[band_number].append(slice_band.colour)

            return possible_bands

        except:
            print("Error trying to identify possible bands")

    # Remove bands that are within bands by removing bands within a certain range of x values.
    def remove_bands_in_bands(self):
        try:
            for slice_number_1 in self.slice_bands:
                for slice_number_2 in self.slice_bands:

                    for slice_band_1 in slice_number_1:
                        for slice_band_2 in slice_number_2:

                            upper_range = slice_band_1.bounding_rectangle.x + (
                                        slice_band_1.bounding_rectangle.width * 0.9)
                            lower_range = slice_band_1.bounding_rectangle.x + (
                                        slice_band_1.bounding_rectangle.width * 0.1)

                            if lower_range < slice_band_1.bounding_rectangle.x < upper_range:
                                slice_number_2.remove(slice_band_2)

        except:
            print("Error removing bands in bands")

    # Removing centroids that are close to each other.
    def remove_false_centroids(self, clusters):
        try:
            centroids = []

            for centroid_number, centroid in clusters.centroids.items():
                centroids.append(centroid[0])

            sorted_centroids = MergeSort().sort(centroids)

            mean_difference = self.find_mean_difference(sorted_centroids)

            previous_centroid = None

            for centroid in sorted_centroids:
                if previous_centroid:
                    difference = centroid - previous_centroid

                    if difference < (mean_difference * 0.4):
                        sorted_centroids.remove(centroid)

                previous_centroid = centroid

            return sorted_centroids

        except:
            print("Error while trying to remove false centroids")

    # Keep trying to find binds with a certain deviation until a sufficient amount has been found.
    def possible_bands(self, sorted_centroids):
        try:
            possible_bands = self.identify_possible_bands(sorted_centroids, 0.1)

            if len(possible_bands) < 5:

                deviation = 0.11

                while len(possible_bands) < 3 and deviation < 0.3:
                    possible_bands = self.identify_possible_bands(sorted_centroids, deviation)

                    deviation += 0.01

            if possible_bands:
                return possible_bands

            else:
                return None

        except:
            raise Exception("Error trying to find possible bands")

    # Remove obvious outlier bands that do not meet certain criteria.
    def remove_outliers(self):
        try:
            for slice_number in self.slice_bands:
                widths = [slice_band.bounding_rectangle.width for slice_band in slice_number]
                heights = [slice_band.bounding_rectangle.height for slice_band in slice_number]

                resistor_height = max(heights)
                mean_band_width = np.mean(widths)

                for slice_band in slice_number[:]:

                    if slice_band.bounding_rectangle.height < (
                            resistor_height * 0.5) or slice_band.bounding_rectangle.width < (mean_band_width * 0.8):
                        slice_number_index = self.slice_bands.index(slice_number)
                        self.slice_bands[slice_number_index].remove(slice_band)

        except:
            print("Error trying to remove outliers")

    # Identifying the possible bands out of the slice bands by only keeping bands that meet certain criteria.
    def find_possible_bands(self):
        try:
            self.remove_outliers()

            self.order_bands()

            self.identify_dupes()
            self.keep_biggest_dupe_band()

            self.remove_bands_in_bands()

            self.order_bands()

            x_list = []

            for slice_number in self.get_bands_attributes()[0]:
                for x in slice_number:
                    x_list.append(x)

            clusters, number_of_bands = self.find_x_cluster(x_list)

            sorted_centroids = self.remove_false_centroids(clusters)
            possible_bands = self.possible_bands(sorted_centroids)

            return possible_bands

        except Exception as error:
            raise Exception(f'Error while selecting slice bands: {error}')
