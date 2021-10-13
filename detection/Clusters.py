import numpy as np
import random as rd
import matplotlib.pyplot as plt
from collections import defaultdict


# https://github.com/pavankalyan1997/Machine-learning-without-any-libraries/blob/master/2.Clustering/1.K_Means_Clustering/K_means_clustering.ipynb
class Kmeans:
    def __init__(self, data, K, number_of_iterations=10):
        self.data = data
        self.groups = {}
        self.centroids = np.array([]).reshape(self.data.shape[1], 0)
        self.K = K
        self.height = self.data.shape[0]
        self.number_of_iterations = number_of_iterations
        self.labels = np.array([])

    def find_centroids(self):
        random_index = rd.randint(0, self.height) - 1

        random_centroids = np.array([self.data[random_index]])

        for cluster_number in range(1, self.K):
            squared_difference_sums = np.array([])

            for item in self.data:

                squared_difference = (item - random_centroids) ** 2
                squared_difference_sum = np.sum(squared_difference)

                squared_difference_sums = np.append(squared_difference_sums, squared_difference_sum)

                #print(f'sd {squared_difference}')
                #print(f'sds {squared_difference_sum}')

            probabilities = squared_difference_sums / np.sum(squared_difference_sums)
            cumulative_probabilities = np.cumsum(probabilities)

            random_decimal = rd.random()

            index = 0

            for probability_index, cumulative_probability in enumerate(cumulative_probabilities):
                if random_decimal < cumulative_probability:
                    index = probability_index
                    break

            random_centroids = np.append(random_centroids, [self.data[index]], axis=0)

        print(random_centroids)

        return random_centroids.T

    def adjust_centroids(self):

        for label_number in range(self.K):
            self.groups[label_number + 1] = np.array([]).reshape(2, 0)

        for item in range(self.height):
            item_label = self.labels[item]

            self.groups[item_label] = np.c_[self.groups[item_label], self.data[item]]

        # Transposing the groups.
        for label_number in range(self.K):
            self.groups[label_number + 1] = self.groups[label_number + 1].T

        for label_number in range(self.K):
            label_items = self.groups[label_number + 1]
            self.centroids[:, label_number] = np.mean(label_items, axis=0)

    def find_distances(self):
        euclidean_distances = None
        # compute euclidean distances and assign clusters
        for iteration_number in range(self.number_of_iterations):

            euclidean_distances = np.array([[0 for k in range(self.K)] for row in range(self.height)])

            for cluster_number in range(self.K):

                differences = self.data - self.centroids[:, cluster_number]

                squared_differences_sum = np.sum(differences ** 2, axis=1)

                for index in range(len(squared_differences_sum)):
                    euclidean_distances[index][cluster_number] = squared_differences_sum[index]

        self.labels = np.argmin(euclidean_distances, axis=1) + 1

        return euclidean_distances

    def fit(self):

        for trial in range(self.number_of_iterations * 10):

            self.centroids = self.find_centroids()

            self.find_distances()

            self.adjust_centroids()

            invalid = False

            for centroid in self.centroids:
                for item in centroid:
                    if item < self.data.min() or item > self.data.max():
                        invalid = True

            if not invalid:
                return self

    def predict(self):
        return self.groups, self.centroids.T

    def WCSS(self):
        wcss = 0
        for k in range(self.K):
            wcss += np.sum((self.groups[k + 1] - self.centroids[:, k]) ** 2)
        return wcss


if __name__ == '__main__':
    data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
            44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
            60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

    data = [[x, 0] for x in data]
    data = np.array(data)

    data = np.array([[1, 2],
                  [1.5, 1.8],
                  [5, 8],
                  [8, 8],
                  [1, 0.6],
                  [9, 11]])

    data = np.zeros((40000, 4))
    data[0:10000] = 30.0
    data[10000:20000] = 60.0
    data[20000:30000] = 90.0
    data[30000:] = 120.0

    plt.scatter(data[:, 0], data[:, 1], c='black', label='unclustered data')

    plt.show()

    results = [8, 30, 44, 60]

    K = 4
    k_means = Kmeans(data, K)

    k_means = k_means.fit()

    print(k_means.centroids)
