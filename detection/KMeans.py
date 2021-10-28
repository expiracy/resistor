import random as rd
import numpy as np


class KMeans:
    def __init__(self, number_of_centroids=4):
        self.number_of_centroids = number_of_centroids
        self.centroids = {}
        self.labels = []

    # Finds the distance between 2 points.
    def find_distance(self, point_1, point_2):
        dx_squared = (point_1[0] - point_2[0]) ** 2
        dy_squared = (point_1[1] - point_2[1]) ** 2
        dz_squared = (point_1[2] - point_2[2]) ** 2

        distance = np.sqrt(dx_squared + dy_squared + dz_squared)

        return distance

    # Finds the distance between items and centroids.
    def find_distance_to_centroids(self, data):
        item_to_centroids_distances = {}

        for centroid_number in range(1, self.number_of_centroids + 1):
            item_to_centroids_distances[centroid_number] = []

        for centroid_number in range(1, self.number_of_centroids + 1):
            for index in range(len(data)):
                item_to_centroid_distance = self.find_distance(data[index], self.centroids[centroid_number])

                item_to_centroids_distances[centroid_number].append(item_to_centroid_distance)

        return item_to_centroids_distances

    # Finds the minimum inter-clusters distance.
    def find_min_inter_cluster_distance(self):
        minimum_inter_cluster_distance = np.inf

        for _, centroid_1 in self.centroids.items():
            for _, centroid_2 in self.centroids.items():

                if centroid_1 != centroid_2 or len(self.centroids) == 1:
                    inter_cluster_distance = self.find_distance(centroid_1, centroid_2)

                    minimum_inter_cluster_distance = min(minimum_inter_cluster_distance, inter_cluster_distance)

        return minimum_inter_cluster_distance

    # Finds the maximum intra-clusters distance.
    def find_max_intra_cluster_distance(self, data_grouped_by_label):
        maximum_intra_cluster_distance = -np.inf

        for centroid_number, data in data_grouped_by_label.items():
            for item in data:
                intra_cluster_distance = self.find_distance(item, self.centroids[centroid_number])

                maximum_intra_cluster_distance = max(maximum_intra_cluster_distance, intra_cluster_distance)

        if maximum_intra_cluster_distance == 0:
            return 1
        else:
            return maximum_intra_cluster_distance

    # Finds the optimal number of clusters using dunn-index.
    def find_optimal_number_of_clusters(self, data):
        dunn_indexes = []

        for centroid_amount in range(1, 10):
            self.centroids = {}
            self.number_of_centroids = centroid_amount
            self.fit(data, self.initialize_centroids(data))

            data_grouped_by_label = self.group_data_by_label(data)

            maximum_intra_cluster_distance = self.find_max_intra_cluster_distance(data_grouped_by_label)

            minimum_inter_cluster_distance = self.find_min_inter_cluster_distance()

            dunn_index = minimum_inter_cluster_distance / maximum_intra_cluster_distance

            dunn_indexes.append(dunn_index)

        optimal_number_of_clusters = np.argmax(dunn_indexes) + 1

        return optimal_number_of_clusters

    # Initialises the seeds to be used for fit().
    def initialize_centroids(self, data):
        number_of_items = data.shape[0]

        centroids = {1: (data[rd.randint(0, number_of_items - 1)])}

        for centroid_number in range(1, self.number_of_centroids):

            minimum_centroid_distances = []

            for item in data:
                minimum_centroid_distance = np.inf

                # Find the distance.
                for _, centroid in centroids.items():
                    centroid_distance = self.find_distance(item, centroid)
                    minimum_centroid_distance = min(minimum_centroid_distance, centroid_distance)

                minimum_centroid_distances.append(minimum_centroid_distance)

            # Item the produces the largest distance is the centroid.
            minimum_centroid_distances = np.array(minimum_centroid_distances)

            next_centroid = data[np.argmax(minimum_centroid_distances)]

            centroids[centroid_number + 1] = next_centroid

        return centroids

    # Labelling items with the number of their closest centroid.
    def find_labels(self, data, intra_cluster_distances_for_centroids):
        self.labels = []

        for item_index in range(len(data)):
            distances_from_centroids = []

            for _, intra_cluster_distances in intra_cluster_distances_for_centroids.items():
                distances_from_centroids.append(intra_cluster_distances[item_index])

            self.labels.append(np.argmin(distances_from_centroids) + 1)

    # Grouping the data by the labels.
    def group_data_by_label(self, data):
        data_grouped_by_label = {}

        for centroid_number in range(1, self.number_of_centroids + 1):
            data_grouped_by_label[centroid_number] = []

        for centroid_number in range(1, self.number_of_centroids + 1):
            for index, label in enumerate(self.labels):
                if label == centroid_number:
                    data_grouped_by_label[centroid_number].append(data[index])

        return data_grouped_by_label

    # Moving centroids by calculating the mean of the data grouped by centroid.
    def move_centroids(self, data_grouped_by_label):
        for centroid_number in range(1, len(data_grouped_by_label) + 1):
            x_total = 0
            y_total = 0
            z_total = 0

            for item in data_grouped_by_label[centroid_number]:
                x_total += item[0]
                y_total += item[1]
                z_total += item[2]

            number_of_items = len(data_grouped_by_label[centroid_number])

            x_mean = x_total / number_of_items
            y_mean = y_total / number_of_items
            z_mean = z_total / number_of_items

            self.centroids[centroid_number] = [x_mean, y_mean, z_mean]

    # Finding the intra-clusters distances for centroids.
    def find_intra_cluster_distances_for_centroids(self, data, centroids):
        intra_cluster_distances_for_centroids = {}

        for centroid_number, centroid in centroids.items():

            intra_cluster_distances = []

            for item in data:
                intra_cluster_distance = self.find_distance(centroid, item)
                intra_cluster_distances.append(intra_cluster_distance)

            intra_cluster_distances_for_centroids[centroid_number] = intra_cluster_distances

        return intra_cluster_distances_for_centroids

    # Checking the centroids have moved by comparing the moved centroids to the initially input centroids.
    def check_if_centroids_moved(self, centroids):
        inter_cluster_distances = []

        for centroid_number in range(1, self.number_of_centroids + 1):

            inter_cluster_distance = np.subtract(self.centroids[centroid_number], centroids[centroid_number])

            inter_cluster_distance_sum = np.sum(inter_cluster_distance)

            inter_cluster_distances.append(abs(inter_cluster_distance_sum))

        inter_cluster_distances_sum = sum(inter_cluster_distances)

        if inter_cluster_distances_sum != 0:
            return True

        else:
            return False

    # K-means algorithm to find the labels and centroids based on the centroids.
    def fit(self, data, centroids, iteration=0, max_iterations=50):
        try:
            self.centroids = {}
            self.labels = []

            intra_cluster_distances_for_cluster = self.find_intra_cluster_distances_for_centroids(data, centroids)

            self.find_labels(data, intra_cluster_distances_for_cluster)

            data_grouped_by_label = self.group_data_by_label(data)

            self.move_centroids(data_grouped_by_label)

            iteration += 1

            centroids_moved = self.check_if_centroids_moved(centroids)

            if iteration == 1 or centroids_moved:
                if iteration <= max_iterations:
                    return self.fit(data, self.centroids, iteration)
                else:
                    return self

            else:
                return self

        except Exception as E:
            print('Error with K value.')
            print(E)