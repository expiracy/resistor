import numpy as np
import random as rd
import matplotlib.pyplot as plt
from collections import defaultdict

#https://github.com/pavankalyan1997/Machine-learning-without-any-libraries/blob/master/2.Clustering/1.K_Means_Clustering/K_means_clustering.ipynb
class Kmeans:
    def __init__(self, X, K):
        self.X = X
        self.Output = {}
        self.centroids = np.array([]).reshape(self.X.shape[1], 0)
        self.K = K
        self.m = self.X.shape[0]

    def find_centroids(self):
        i = rd.randint(0, X.shape[0])

        centroid_temp = np.array([X[i]])

        for k in range(1, self.K):
            D = np.array([])

            for x in self.X:
                D = np.append(D, np.min(np.sum((x - centroid_temp) ** 2)))

            prob = D / np.sum(D)
            cumulative_prob = np.cumsum(prob)

            r = rd.random()

            i = 0

            for j, p in enumerate(cumulative_prob):
                if r < p:
                    i = j
                    break

            centroid_temp = np.append(centroid_temp, [self.X[i]], axis=0)

        return centroid_temp.T

    def fit(self, n_iter):
        # randomly Initialize the centroids
        self.centroids = self.find_centroids()

        # compute euclidian distances and assign clusters
        for n in range(n_iter):

            EuclideanDistance = np.array([]).reshape(self.m, 0)

            for k in range(self.K):

                differences = np.sum((self.X - self.centroids[:, k]) ** 2, axis=1)

                EuclideanDistance = np.c_[EuclideanDistance, differences]

            C = np.argmin(EuclideanDistance, axis=1) + 1

            # adjust the centroids
            Y = {}

            for k in range(self.K):
                Y[k + 1] = np.array([]).reshape(2, 0)

            for i in range(self.m):
                Y[C[i]] = np.c_[Y[C[i]], self.X[i]]

            for k in range(self.K):
                Y[k + 1] = Y[k + 1].T

            for k in range(self.K):
                self.centroids[:, k] = np.mean(Y[k + 1], axis=0)

            self.Output = Y

    def predict(self):
        return self.Output, self.centroids.T

    def WCSS(self):
        wcss = 0
        for k in range(self.K):
            wcss += np.sum((self.Output[k + 1] - self.centroids[:, k]) ** 2)
        return wcss


x_list = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 60, 8, 29, 60, 8, 29, 60]
X = [[x, 0] for x in x_list]
X = np.array(X)


plt.scatter(X[:, 0], X[:, 1], c='black', label='unclustered data')
#plt.show()

K = 4
k_means = Kmeans(X, K)
k_means.fit(10)
output, centroids = k_means.predict()

print(centroids)


