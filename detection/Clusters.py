import numpy as np
import random as rd
import matplotlib.pyplot as plt


class Kmeans:
    def __init__(self, data, K):
        self.data = data
        self.Output = {}
        self.Centroids = np.array([]).reshape(self.data.shape[1], 0)
        self.K = K
        self.height = self.data.shape[0]

    def kmeanspp(self):
        i = rd.randint(0, self.data.shape[0])
        Centroid_temp = np.array([self.data[i]])
        for k in range(1, self.K):
            D = np.array([])
            for x in self.data:
                D = np.append(D, np.min(np.sum((x - Centroid_temp) ** 2)))
            prob = D / np.sum(D)
            cummulative_prob = np.cumsum(prob)
            r = rd.random()
            i = 0
            for j, p in enumerate(cummulative_prob):
                if r < p:
                    i = j
                    break
            Centroid_temp = np.append(Centroid_temp, [self.data[i]], axis=0)
        return Centroid_temp.T

    def euclidian_distance(self):
        pass

    def fit(self, n_iter):
        # randomly Initialize the centroids
        self.Centroids = self.kmeanspp()

        """for i in range(self.K):
            rand=rd.randint(0,self.m-1)
            self.Centroids=np.c_[self.Centroids,self.X[rand]]"""

        # compute euclidian distances and assign clusters
        for n in range(n_iter):
            EuclidianDistance = np.array([]).reshape(self.height, 0)
            for k in range(self.K):
                tempDist = np.sum((self.data - self.Centroids[:, k]) ^ 2, axis=1)

                EuclidianDistance = np.c_[EuclidianDistance, tempDist]

            C = np.argmin(EuclidianDistance, axis=1) + 1

            # adjust the centroids
            Y = {}

            for k in range(self.K):
                Y[k + 1] = np.array([]).reshape(2, 0)

            for i in range(self.height):
                Y[C[i]] = np.c_[Y[C[i]], self.data[i]]

            for k in range(self.K):
                Y[k + 1] = Y[k + 1].T

            for k in range(self.K):
                self.Centroids[:, k] = np.mean(Y[k + 1], axis=0)

            self.Output = Y



    def predict(self):
        return self.Output, self.Centroids.T

    def WCSS(self):
        wcss = 0
        for k in range(self.K):
            wcss += np.sum((self.Output[k + 1] - self.Centroids[:, k]) ** 2)
        return wcss


x_list = [30, 61, 30, 61, 30, 61, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 30, 44, 60, 8, 30, 44, 60, 8, 30, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 44, 60, 8, 29, 60, 8, 29, 60, 8, 29, 60]
x_y_list = [[x, 0] for x in x_list]
x_y_list = np.array(x_y_list)


plt.scatter(x_y_list[:, 0], x_y_list[:, 1], c='black', label='unclustered data')
plt.show()

k_means = Kmeans(x_y_list, 4)

k_means.fit(10)

output, centroids = k_means.predict()

color = ['red', 'blue', 'green', 'cyan', 'magenta']
labels = ['cluster1', 'cluster2', 'cluster3', 'cluster4', 'cluster5']

print(centroids)

for k in range(4):
    plt.scatter(output[k+1][:, 0], output[k+1][:, 1], c=color[k], label=labels[k])

for centroid in centroids:
    plt.scatter(centroid[0], centroid[1], s=100, c='yellow', label='Centroids')

plt.show()

print("BREAK")
