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
        self.centroids = {}
        self.labels = []

    # function to compute euclidean distance
    def find_distance(self, point_1, point_2):
        dx = (point_1[0] - point_2[0]) ** 2
        dy = (point_1[1] - point_2[1]) ** 2
        distance = np.sqrt(dx + dy)

        return distance

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
    def find_seeds(self):
        ## initialize the centroids list and add
        ## a randomly selected data point to the list
        seeds = []
        seeds.append(self.data[np.random.randint(self.data.shape[0]), :])

        ## compute remaining k - 1 centroids
        for centroid_number in range(self.number_of_clusters - 1):

            ## initialize a list to store distances of data
            ## points from nearest centroid
            dist = []
            for i in range(self.data.shape[0]):
                point = self.data[i, :]
                d = sys.maxsize

                ## compute distance of 'point' from each of the previously
                ## selected centroid and store the minimum distance
                for j in range(len(seeds)):
                    temp_dist = self.find_distance(point, seeds[j])
                    d = min(d, temp_dist)
                dist.append(d)

            ## select data point with maximum distance as our next centroid
            dist = np.array(dist)
            next_centroid = self.data[np.argmax(dist), :]
            seeds.append(next_centroid)

        print(seeds)
        return seeds

    def fit(self):
        seeds = self.find_seeds()

        Centroids = pd.DataFrame(data=seeds, columns=["X", "Y"])
        Values = pd.DataFrame(data=self.data, columns=["X", "Y"])

        diff = 1
        j = 0

        while diff != 0:
            centroid_number = 1
            centroids_distances = {}

            for seed in seeds:

                distances = []

                for item in self.data:
                    distance = self.find_distance(seed, item)
                    distances.append(distance)

                Values[centroid_number] = distances
                centroids_distances[centroid_number] = distances

                centroid_number += 1

            C = []

            self.labels = []

            for item_index in range(len(self.data)):
                distances_from_centroids = []
                for centroid, distances_from_centroid in centroids_distances.items():
                    distances_from_centroids.append(distances_from_centroid[item_index])

                self.labels.append(distances_from_centroids.index(min(distances_from_centroids)) + 1)

            for index, row in Values.iterrows():
                min_dist = row[1]
                pos = 1
                for i in range(K):
                    if row[i + 1] < min_dist:
                        min_dist = row[i + 1]
                        pos = i + 1


                C.append(pos)

            data_grouped_by_label = {}

            for cluster_number in range(1, self.number_of_clusters + 1):
                data_grouped_by_label[cluster_number] = []

            for cluster_number in range(1, self.number_of_clusters + 1):
                for index, label in enumerate(self.labels):
                    if label == cluster_number:
                        data_grouped_by_label[cluster_number].append(self.data[index])

                print(data_grouped_by_label[cluster_number])

                self.centroids[cluster_number] = [np.mean(data_grouped_by_label[cluster_number], axis=0), np.mean(data_grouped_by_label[cluster_number], axis=1)]

            print(self.centroids)






            Values["Cluster"] = C

            Centroids_new = Values.groupby(["Cluster"]).mean()[["Y", "X"]]
            print(Centroids_new)
            if j == 0:
                diff = 1
                j = j + 1
            else:
                diff = (Centroids_new['Y'] - Centroids['Y']).sum() + (Centroids_new['X'] - Centroids['X']).sum()
                print(diff.sum())
            Centroids = Values.groupby(["Cluster"]).mean()[["Y", "X"]]

        print(Centroids)


if __name__ == "__main__":
    data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
            44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
            60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

    original = [[x, 0] for x in data]

    # Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

    # number of clusters
    K = 4

    # Select random observation as centroids
    k_means = KMeans2(np.array(original), 4)

    k_means.fit()
    print(k_means.centroids)