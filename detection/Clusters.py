import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rd
from collections import defaultdict
import matplotlib.cm as cm
from random import sample

'''
https://mail.google.com/mail/u/0/#inbox/QgrcJHrhzcthLxKswsPWMfSKrFMbFWbWWlv

DO THIS
'''


#https://github.com/pavankalyan1997/Machine-learning-without-any-libraries/blob/master/2.Clustering/1.K_Means_Clustering/K_means_clustering.ipynb


class Kmeans:
    def __init__(self, X, K):
        self.X = X
        self.Output = {}
        self.Centroids = np.array([]).reshape(self.X.shape[1], 0)
        self.K = K
        self.m = self.X.shape[0]

    def kmeanspp(self, X, K):
        i = rd.randint(0, X.shape[0])
        Centroid_temp = np.array([X[i - 1]])
        for k in range(1, K):
            D = np.array([])
            for x in X:
                D = np.append(D, np.min(np.sum((x - Centroid_temp) ** 2)))
            prob = D / np.sum(D)
            cummulative_prob = np.cumsum(prob)
            r = rd.random()
            i = 0
            for j, p in enumerate(cummulative_prob):
                if r < p:
                    i = j
                    break
            Centroid_temp = np.append(Centroid_temp, [X[i]], axis=0)
        return Centroid_temp.T

    def fit(self, n_iter):
        # randomly Initialize the centroids
        self.Centroids = self.kmeanspp(self.X, self.K)

        """for i in range(self.K):
            rand=rd.randint(0,self.m-1)
            self.Centroids=np.c_[self.Centroids,self.X[rand]]"""

        # compute euclidian distances and assign clusters
        for n in range(n_iter):
            EuclidianDistance = np.array([]).reshape(self.m, 0)
            for k in range(self.K):
                tempDist = np.sum((self.X - self.Centroids[:, k]) ** 2, axis=1)
                EuclidianDistance = np.c_[EuclidianDistance, tempDist]
            C = np.argmin(EuclidianDistance, axis=1) + 1
            # adjust the centroids
            Y = {}
            for k in range(self.K):
                Y[k + 1] = np.array([]).reshape(2, 0)
            for i in range(self.m):
                Y[C[i]] = np.c_[Y[C[i]], self.X[i]]

            for k in range(self.K):
                Y[k + 1] = Y[k + 1].T
            for k in range(self.K):
                self.Centroids[:, k] = np.mean(Y[k + 1], axis=0)

            self.Output = Y

    def predict(self):
        return self.Output, self.Centroids.T

    def calculate_cluster_square_sum(self):
        wcss = 0
        for k in range(self.K):
            wcss += np.sum((self.Output[k + 1] - self.Centroids[:, k]) ** 2)
        return wcss

    def get_kmeans_pp_centroids(self, X1, k=5):
        centroids = random.sample(X1, 4)
        print(centroids)
        i = 1
        dist = []
        while i != k:
            max_dist = [0, 0]
            # go through the centroids
            for index, row in centroids.iterrows():
                # calculate distance of every centroid with every other data point
                d = np.sqrt((X1["Height"] - row["Height"]) ** 2 + (X1["Weight"] - row["Weight"]) ** 2)
                # check which centroid has a max distance with another point
                if max(d) > max(max_dist):
                    max_dist = d

            X1 = pd.concat([X1, max_dist], axis=1)
            idx = X1.iloc[:, i + 1].idxmax()
            max_coor = pd.DataFrame(X1.iloc[idx][["Height", "Weight"]]).T
            centroids = pd.concat([centroids, max_coor])
            X1 = X1.drop(idx)
            i += 1

        print(centroids)
        return centroids

if __name__ == '__main__':
    data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 60, 8, 29, 60, 8, 29, 60]
    data = [[x, 0] for x in data]
    X = np.array(data)

    m = X.shape[0]
    n_iter = 100

    K = 4
    k_means = Kmeans(X, K)
    centroids = k_means.get_kmeans_pp_centroids(X)
    ret = k_means.predict()

