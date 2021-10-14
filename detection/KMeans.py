import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
import sys

# data = pd.read_csv('clustering.csv')
# data.head()

class KMeans2:
    def __init__(self, number_of_centroids=2):
        self.number_of_centroids = number_of_centroids
        self.centroids = {}
        self.labels = []

    # function to compute euclidean distance
    def find_distance(self, point_1, point_2):
        dx = (point_1[0] - point_2[0]) ** 2
        dy = (point_1[1] - point_2[1]) ** 2
        distance = np.sqrt(dx + dy)

        return distance

    def find_optimal_k(self, data):
        distortions = []

        for centroid_count in range(1, 10):
            self.centroids = {}
            centroids = []

            self.number_of_centroids = centroid_count
            self.fit(data)

            if self.centroids:
                for centroid_count_2, centroid in self.centroids.items():
                    centroids.append(centroid)

            centroids = np.array(centroids)

            centroid_count_3 = 1
            distances = np.zeros((self.number_of_centroids, len(data)))
            print(distances)

            for index in range(len(data)):
                distances[centroid_count_3][index] = self.find_distance(data[index], self.centroids[centroid_count_3])

            test = cdist(data, centroids, 'euclidean')


            distortions.append(sum(np.min(cdist(data, centroids, 'euclidean'), axis=1)) / data.shape[0])

        # Plot the elbow
        plt.plot(range(1, len(distortions) + 1), distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()

    # initialization algorithm
    def find_seeds(self, data):
        ## initialize the centroids list and add
        ## a randomly selected data point to the list
        seeds = {}
        seeds[1] = (data[np.random.randint(data.shape[0]), :])

        ## compute remaining k - 1 centroids
        for centroid_count in range(self.number_of_centroids - 1):

            ## initialize a list to store distances of data
            ## points from nearest centroid
            dist = []
            for i in range(data.shape[0]):
                point = data[i, :]
                d = sys.maxsize

                ## compute distance of 'point' from each of the previously
                ## selected centroid and store the minimum distance
                for j in range(1, len(seeds) + 1):
                    temp_dist = self.find_distance(point, seeds[j])
                    d = min(d, temp_dist)
                dist.append(d)

            ## select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_centroid = data[np.argmax(dist), :]
            seeds[centroid_count + 2] = next_centroid

        return seeds

    def fit(self, data):
        try:
            seeds = self.find_seeds(data)

            difference = 1
            iteration = 0

            while difference != 0:
                centroid_count = 1
                centroids_distances = {}

                for seed_number, seed in seeds.items():

                    distances = []

                    for item in data:
                        distance = self.find_distance(seed, item)
                        distances.append(distance)

                    centroids_distances[centroid_count] = distances

                    centroid_count += 1

                self.labels = []

                for item_index in range(len(data)):
                    distances_from_centroids = []
                    for centroid, distances_from_centroid in centroids_distances.items():
                        distances_from_centroids.append(distances_from_centroid[item_index])

                    self.labels.append(distances_from_centroids.index(min(distances_from_centroids)) + 1)

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

        except:
            print("Error due to K value.")

if __name__ == "__main__":
    data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
            44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
            60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

    original = [[x, 0] for x in data]

    # Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

    # number of clusters
    K = 4

    # Select random observation as centroids
    k_means = KMeans2(4)
    k_means.find_optimal_k(np.array(original))

    k_means.fit(np.array(original))
    print(k_means.centroids)