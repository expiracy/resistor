import numpy as np
from sklearn.cluster import KMeans

class SliceBands:
    def __init__(self):
        self.list = []

    def find_resistor_bands(self):
        x_list = self.bands_attributes()[0]
        self.remove_outliers(x_list)

        print("dsjhidhakd")

    def bands_attributes(self):

        x_list = []
        y_list = []
        widths = []
        heights = []
        colours = []

        for bands_for_slice in self.list:
            for bands in bands_for_slice:
                x_list.append(bands.bounding_rectangle.x)
                y_list.append(bands.bounding_rectangle.y)
                widths.append(bands.bounding_rectangle.width)
                heights.append(bands.bounding_rectangle.height)
                colours.append(bands.colour)

        return x_list, y_list, widths, heights, colours

    def remove_outliers(self, array):

        array = np.reshape(array, (1, -1)).T

        mean = np.mean(array)
        print(mean)

        Kmean = KMeans(n_clusters=5)

        Kmean.fit(array)
        labels = Kmean.labels_
        var = Kmean.cluster_centers_
        print(var)
        print(labels)


