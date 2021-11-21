import numpy as np

from detection.KMeans import KMeans
from detection.MergeSort import MergeSort
from detection.SliceBands import SliceBands


# Initiates with slice bands and carries out operations to select only the most likely slice bands.
class SliceBandsFilter:
    def __init__(self, slice_bands=None):
        self.slice_bands = slice_bands

    # Using K-means to find where there are clusters of X (locating the band).
    def find_x_cluster(self, x_list, number_of_bands):
        try:
            x_y_z_list = np.array([[x, 0, 0] for x in x_list])

            k_means = KMeans()

            if number_of_bands is None:
                number_of_bands = k_means.find_optimal_number_of_clusters(x_y_z_list)

                if number_of_bands > 6 or number_of_bands < 3:
                    number_of_bands = 4

            k_means.number_of_centroids = number_of_bands

            clusters = k_means.fit(x_y_z_list, k_means.initialize_centroids(x_y_z_list))

            return clusters, number_of_bands

        except Exception as error:
            raise Exception(f'Error while trying to find x cluster, {error}')

    # Finds the mean difference for a list.
    def find_mean_difference(self, list):
        try:
            differences = np.diff(list)
            mean_difference = np.mean(differences)

            return mean_difference

        except Exception as error:
            raise Exception(f'Error while trying to find mean difference, {error}')

    # Identifying the slice bands that match up with the x centroids.
    def identify_possible_bands(self, sorted_centroids, deviation):
        try:
            possible_bands = {}

            for possible_band in range(len(sorted_centroids)):
                possible_bands[possible_band] = []

            mean_centroid_difference = self.find_mean_difference(sorted_centroids)

            for band_number, centroid in enumerate(sorted_centroids):
                for slice_band in self.slice_bands.list():
                    centroid_band_difference = abs(slice_band.bounding_rectangle.x - centroid)
                    if centroid_band_difference < mean_centroid_difference * deviation:
                        possible_bands[band_number].append(slice_band)

            return possible_bands

        except Exception as error:
            print(f'identify_possible_bands(), {error}')

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

                    if difference < (mean_difference * 0.2):
                        sorted_centroids.remove(centroid)

                previous_centroid = centroid

            return sorted_centroids

        except Exception as error:
            print(f'remove_false_centroids(), {error}')

    # Keep trying to find binds with a certain deviation until a sufficient amount has been found.
    def possible_bands(self, sorted_centroids):
        try:
            possible_bands = self.identify_possible_bands(sorted_centroids, 0.2)

            if len(min(possible_bands.values(), key=len)) < 5:

                deviation = 0.21

                while len(min(possible_bands.values(), key=len)) < 3 and deviation < 0.3:
                    possible_bands = self.identify_possible_bands(sorted_centroids, deviation)

                    deviation += 0.01

            if possible_bands:
                return possible_bands

            else:
                return None

        except Exception as error:
            print(f'possible_bands(), {error}')
            raise Exception(f'Error trying to find possible bands, {error}')

    # Remove obvious outlier bands that do not meet certain criteria.
    def remove_short_bands(self):
        try:
            self.slice_bands.remove_short_bands()

        except Exception as error:
            print(f'remove_short_bands(), {error}')

    # Remove obvious outlier bands that do not meet certain criteria.
    def remove_narrow_bands(self):
        try:
            self.slice_bands.remove_narrow_bands()

        except Exception as error:
            print(f'remove_narrow_bands(), {error}')

    # Identifying the possible bands out of the slice bands by only keeping bands that meet certain criteria.
    def find_possible_bands(self, number_of_bands):
        try:
            clusters, number_of_bands = self.find_x_cluster(self.slice_bands.get_x_centres(), number_of_bands)

            sorted_centroids = self.remove_false_centroids(clusters)
            possible_bands = self.possible_bands(sorted_centroids)

            return SliceBands().load_slice_band_groups(possible_bands)

        except Exception as error:
            raise Exception(f'Error finding possible bands, {error}')
