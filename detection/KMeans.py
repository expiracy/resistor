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
    def __init__(self, data, number_of_clusters):
        self.data = data
        self.number_of_clusters = number_of_clusters
        self.centroids = self.find_centroids()

    # function to compute euclidean distance
    def find_distance(self, point_1, point_2):
        return np.sum((point_1 - point_2) ** 2)

    def find_optimal_k(self):
        distortions = []
        K = range(1, 10)
        for k in K:
            kmeanModel = KMeans(n_clusters=k).fit(self.data)
            kmeanModel.fit(self.data)
            distortions.append(sum(np.min(cdist(self.data, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / self.data.shape[0])

        # Plot the elbow
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()

    # initialization algorithm
    def find_centroids(self):
        ## initialize the centroids list and add
        ## a randomly selected data point to the list
        centroids = []
        centroids.append(self.data[np.random.randint(self.data.shape[0]), :])

        ## compute remaining k - 1 centroids
        for c_id in range(self.number_of_clusters - 1):

            ## initialize a list to store distances of data
            ## points from nearest centroid
            dist = []
            for i in range(self.data.shape[0]):
                point = self.data[i, :]
                d = sys.maxsize

                ## compute distance of 'point' from each of the previously
                ## selected centroid and store the minimum distance
                for j in range(len(centroids)):
                    temp_dist = self.find_distance(point, centroids[j])
                    d = min(d, temp_dist)
                dist.append(d)

            ## select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_centroid = self.data[np.argmax(dist), :]
            centroids.append(next_centroid)

        return centroids

    def fit(self):

        Centroids = pd.DataFrame(data=self.centroids, columns=["X", "Y"])
        Values = pd.DataFrame(data=self.data, columns=["X", "Y"])

        diff = 1
        j = 0

        while (diff != 0):
            XD = Values
            i = 1
            for index1, row_c in Centroids.iterrows():
                ED = []
                for index2, row_d in XD.iterrows():
                    dx = (row_c["X"] - row_d["X"]) ** 2
                    dy = (row_c["Y"] - row_d["Y"]) ** 2
                    distance = np.sqrt(dx + dy)
                    ED.append(distance)
                Values[i] = ED
                i = i + 1

            C = []
            for index, row in Values.iterrows():
                min_dist = row[1]
                pos = 1
                for i in range(K):
                    if row[i + 1] < min_dist:
                        min_dist = row[i + 1]
                        pos = i + 1
                C.append(pos)
            Values["Cluster"] = C
            Centroids_new = Values.groupby(["Cluster"]).mean()[["Y", "X"]]
            if j == 0:
                diff = 1
                j = j + 1
            else:
                diff = (Centroids_new['Y'] - Centroids['Y']).sum() + (Centroids_new['X'] - Centroids['X']).sum()
                print(diff.sum())
            Centroids = Values.groupby(["Cluster"]).mean()[["Y", "X"]]

        print(Centroids)


data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
        44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
        60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

original = [[x, 0] for x in data]

# Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

# number of clusters
K = 4

# Select random observation as centroids
k_means = KMeans2(np.array(original), 6)

k_means.fit()
print(k_means.centroids)
