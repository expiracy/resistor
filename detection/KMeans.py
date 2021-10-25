import random as rd
import matplotlib.pyplot as plt
import numpy as np
from detection.Graph import Graph
from detection.Line import Line

class KMeans:
    def __init__(self, number_of_centroids=2):
        self.number_of_centroids = number_of_centroids
        self.centroids = {}
        self.labels = []


    # function to compute euclidean distance
    def find_distance(self, point_1, point_2):
        dx_squared = (point_1[0] - point_2[0]) ** 2
        dy_squared = (point_1[1] - point_2[1]) ** 2

        distance = np.sqrt(dx_squared + dy_squared)

        return distance

    # Function to find the optimal number of clusters for data.
    def find_optimal_k(self, data, mode='optimal'):
        try:
            deviations = []

            # Run K-means for every value of K in range 1, 10.
            for centroid_number in range(1, 10):

                self.centroids = {}
                centroids_distances = {}

                self.number_of_centroids = centroid_number
                self.fit(data)

                # Create dictionary to hold the distance values.
                if len(self.centroids) == centroid_number:
                    for centroid_number_2 in range(1, self.number_of_centroids + 1):
                        centroids_distances[centroid_number_2] = []

                    # Calculate the distance between every centroid to every item and append it to the corresponding cluster dictionary list.
                    for centroid_number_2 in range(1, self.number_of_centroids + 1):
                        for index in range(len(data)):
                            centroid_distance = self.find_distance(data[index], self.centroids[centroid_number_2])

                            centroids_distances[centroid_number_2].append(centroid_distance)

                    # Find the minimum cluster distance for each item and append it to the minimum distances list.
                    minimum_distances = []

                    for item in range(len(data)):
                        item_distances = []

                        for centroid_number_2 in range(1, self.number_of_centroids + 1):
                            item_distances.append(centroids_distances[centroid_number_2][item])

                        minimum_distances.append(np.min(item_distances))

                    # Find the sum of all the minimum cluster distances for a value of K and append it to the distortions list.
                    sum_minimum_distances = np.sum(minimum_distances)

                    deviations.append((sum_minimum_distances / len(data)) ** 2)

            # Plotting the resulting elbow graph.
            #Graph().graph_x_against_y(list(range(1, len(deviations) + 1)), deviations, 'k', 'Deviation', 'Elbow Method Graph')

            if mode == 'optimal':
                for deviation in deviations:
                    if deviation < 1:
                        optimal_k = deviations.index(deviation) + 1

                        return optimal_k

            else:
                return len(deviations) + 1

        except ValueError:
            print("Value of K higher than number of distinct clusters.")
            return None

    # initialization algorithm
    def initialize_centroids(self, data):
        number_of_items = data.shape[0]

        # Randomly choose the first cluster.
        seeds = {1: (data[rd.randint(0, number_of_items - 1)])}

        # Identify the rest of the clusters.
        for centroid_number in range(1, self.number_of_centroids):

            minimum_seed_distances = []

            for item in data:
                minimum_seed_distance = np.inf

                # Find the distance.
                for seed_number, seed in seeds.items():
                    seed_distance = self.find_distance(item, seed)
                    minimum_seed_distance = min(minimum_seed_distance, seed_distance)

                minimum_seed_distances.append(minimum_seed_distance)

            # Item the produces the largest distance is the centroid.
            minimum_seed_distances = np.array(minimum_seed_distances)

            next_seed = data[np.argmax(minimum_seed_distances)]

            seeds[centroid_number + 1] = next_seed

        return seeds

    # Labelling items with their closest centroid.
    def find_labels(self, centroids_distances, data):

        self.labels = []

        for item_index in range(len(data)):
            distances_from_centroids = []

            for centroid, distances_from_centroid in centroids_distances.items():
                distances_from_centroids.append(distances_from_centroid[item_index])

            self.labels.append(distances_from_centroids.index(min(distances_from_centroids)) + 1)

    # K-means algorithm to find the centroids based on the seeds.
    def fit(self, data):

        try:
            seeds = self.initialize_centroids(data)

            difference = 1
            iteration = 0

            while difference != 0:
                centroid_number = 1
                centroids_distances = {}

                for seed_number, seed in seeds.items():

                    seed_distances = []

                    for item in data:
                        seed_distance = self.find_distance(seed, item)
                        seed_distances.append(seed_distance)

                    centroids_distances[centroid_number] = seed_distances

                    centroid_number += 1

                self.find_labels(centroids_distances, data)

                data_grouped_by_label = {}

                for cluster_number in range(1, self.number_of_centroids + 1):
                    data_grouped_by_label[cluster_number] = []

                for cluster_number in range(1, self.number_of_centroids + 1):
                    for index, label in enumerate(self.labels):
                        if label == cluster_number:
                            data_grouped_by_label[cluster_number].append(data[index])

                    x_total = 0
                    y_total = 0

                    for item in data_grouped_by_label[cluster_number]:
                        x_total += item[0]
                        y_total += item[1]

                    number_of_items = len(data_grouped_by_label[cluster_number])

                    x_mean = x_total / number_of_items
                    y_mean = y_total / number_of_items

                    self.centroids[cluster_number] = [x_mean, y_mean]

                if iteration == 0:
                    difference = 1
                    iteration += 1

                else:
                    cluster_seed_difference_sums = []

                    for cluster_number in range(1, self.number_of_centroids + 1):
                        cluster_seed_difference = np.subtract(self.centroids[cluster_number], seeds[cluster_number])
                        cluster_seed_difference_sum = np.sum(cluster_seed_difference)
                        cluster_seed_difference_sums.append(cluster_seed_difference_sum)

                    difference = sum(cluster_seed_difference_sums)

                    seeds = self.centroids

            return self

        except:
            print("Error due to K value.")


if __name__ == "__main__":
    data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
            44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
            60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

    original = [[x, 0] for x in data]
    original = np.array(original)
    '''
    original = np.zeros((100, 2))
    original[0:10] = 1
    original[10:25] = 5
    original[25:50] = 6
    original[50:75] = 8
    original[75:100] = 15
    '''
    # Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

    # number of clusters

    # Select random observation as centroids
    test = KMeans().find_optimal_k(original)
    print(test)



