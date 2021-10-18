import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

# data = pd.read_csv('clustering.csv')
# data.head()
# function to compute euclidean distance


data = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30,
        44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44,
        60, 8, 29, 60, 8, 29, 60, 8, 29, 60]

K = 4

original = [[x, 0] for x in data]
original = np.array(original)
Values = pd.DataFrame(data=original, columns=["X", "Y"])
Centroids = (Values.sample(n=K))
Centroids = [[29,  0], [61,  0], [8, 0], [44,  0]]
Centroids = pd.DataFrame(data=Centroids, columns=["X", "Y"])


# Step 3 - Assign all the points to the closest cluster centroid
# Step 4 - Recompute centroids of newly formed clusters
# Step 5 - Repeat step 3 and 4

diff = 1
j = 0

while (diff != 0):
    print(diff)
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
        print("OLD\n", Centroids)
        print("NEW\n", Centroids_new)
        diff = (Centroids_new['Y'] - Centroids['Y']).sum() + (Centroids_new['X'] - Centroids['X']).sum()
        print(diff)
    Centroids = Values.groupby(["Cluster"]).mean()[["Y", "X"]]

print(Centroids)