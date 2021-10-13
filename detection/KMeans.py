import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

import sys

# data = pd.read_csv('clustering.csv')
# data.head()

class K_means:
    def __init__(self, data, number_of_clusters):
        self.number_of_clusters = number_of_clusters


# function to plot the selected centroids
def plot(data, centroids):
    plt.scatter(data[:, 0], data[:, 1], marker='.',
                color='gray', label='data points')
    plt.scatter(centroids[:-1, 0], centroids[:-1, 1],
                color='black', label='previously selected centroids')
    plt.scatter(centroids[-1, 0], centroids[-1, 1],
                color='red', label='next centroid')
    plt.title('Select % d th centroid' % (centroids.shape[0]))

    plt.legend()
    plt.xlim(-5, 12)
    plt.ylim(-10, 15)
    plt.show()


# function to compute euclidean distance
def find_distance(p1, p2):
    return np.sum((p1 - p2) ** 2)

# initialization algorithm
def initialize(data, k):
    '''
    initialized the centroids for K-means++
    inputs:
        data - numpy array of data points having shape (200, 2)
        k - number of clusters
    '''
    ## initialize the centroids list and add
    ## a randomly selected data point to the list
    centroids = []
    centroids.append(data[np.random.randint(
        data.shape[0]), :])
    plot(data, np.array(centroids))

    ## compute remaining k - 1 centroids
    for c_id in range(k - 1):

        ## initialize a list to store distances of data
        ## points from nearest centroid
        dist = []
        for i in range(data.shape[0]):
            point = data[i, :]
            d = sys.maxsize

            ## compute distance of 'point' from each of the previously
            ## selected centroid and store the minimum distance
            for j in range(len(centroids)):
                temp_dist = find_distance(point, centroids[j])
                d = min(d, temp_dist)
            dist.append(d)

        ## select data point with maximum distance as our next centroid
        dist = np.array(dist)
        next_centroid = data[np.argmax(dist), :]
        centroids.append(next_centroid)
        dist = []
        plot(data, np.array(centroids))
    return centroids


data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
        44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
        60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

original = [[x, 0] for x in data]

Values = pd.DataFrame(data=original, columns=["X", "Y"])
# Visualise data points
plt.scatter(Values["X"], Values["Y"], c='black')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.show()

# Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

# number of clusters
K = 4

# Select random observation as centroids
Centroids = (Values.sample(n=K))
plt.scatter(Values["X"], Values["Y"], c='black')
plt.scatter(Centroids["X"], Centroids["Y"], c='red')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.show()

# Step 3 - Assign all the points to the closest cluster centroid
# Step 4 - Recompute centroids of newly formed clusters
# Step 5 - Repeat step 3 and 4

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
        # print(diff.sum())
    Centroids = Values.groupby(["Cluster"]).mean()[["Y", "X"]]

color = ['blue', 'green', 'cyan', 'orange']

for k in range(K):
    data = Values[Values["Cluster"] == k + 1]
    plt.scatter(data["X"], data["Y"], c=color[k])


plt.scatter(Centroids["X"], Centroids["Y"], c='red')
plt.xlabel('Income')
plt.ylabel('Y values')
plt.show()

pog = np.array(original)
for i in range(100):
    centroids = initialize(pog, K)
    print(centroids)
