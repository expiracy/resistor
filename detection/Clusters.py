import numpy as np
import random as rd
import matplotlib.pyplot as plt
from collections import defaultdict

#https://github.com/pavankalyan1997/Machine-learning-without-any-libraries/blob/master/2.Clustering/1.K_Means_Clustering/K_means_clustering.ipynb
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
        index = rd.randint(0, self.height) - 1

        centroid_temp = np.array([X[index]])

        for k in range(1, self.K):
            D = np.array([])

            for x in self.data:
                D = np.append(D, np.min(np.sum((x - centroid_temp) ** 2)))

            prob = D / np.sum(D)
            cumulative_prob = np.cumsum(prob)

            r = rd.random()

            i = 0

            for j, p in enumerate(cumulative_prob):
                if r < p:
                    i = j
                    break

            centroid_temp = np.append(centroid_temp, [self.data[i]], axis=0)

        return centroid_temp.T

    def adjust_centroids(self):

        for cluster_number in range(self.K):
            self.groups[cluster_number + 1] = np.array([]).reshape(2, 0)

        for index in range(self.height):
            self.groups[self.labels[index]] = np.c_[self.groups[self.labels[index]], self.data[index]]

        for cluster_number in range(self.K):
            self.groups[cluster_number + 1] = self.groups[cluster_number + 1].T

        for cluster_number in range(self.K):
            self.centroids[:, cluster_number] = np.mean(self.groups[cluster_number + 1], axis=0)


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

    def find_clusters(self):
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


x_list = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 60, 8, 29, 60, 8, 29, 60]
X = [[x, 0] for x in x_list]
X = np.array(X)

print(X)

plt.scatter(X[:, 0], X[:, 1], c='black', label='unclustered data')

results = [8, 30, 44, 60]

K = 4
k_means = Kmeans(X, K)

k_means = k_means.find_clusters()
print(k_means.labels)
print(k_means.groups)
print(k_means.centroids)
