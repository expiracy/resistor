import cv2
from detection.BoundingRectangle import BoundingRectangle
from detection.Greyscale import Greyscale
from detection.BGR import BGR
from detection.HSV import HSV
from detection.HSVRange import HSVRange
from detection.BoundingRectangle import BoundingRectangle
from sklearn.cluster import KMeans
from detection.Colour import Colour
from detection.HSVRange import HSVRange


import numpy as np


class Glare:
    def __init__(self, image):
        self.image = image

    def show_colour_clusters(self, clusters):

        centroids = clusters.cluster_centers_

        labels = np.arange(0, len(np.unique(clusters.labels_)) + 1)

        hist, _ = np.histogram(clusters.labels_, bins=labels)
        hist = hist.astype("float")
        hist /= hist.sum()

        colours = [(percent, colour) for percent, colour in zip(hist, centroids)]

        sorted_colours = sorted(colours)

        # Create frequency rect and iterate through each clusters's color and percentage
        rectangle = np.zeros((50, 300, 3), dtype=np.uint8)

        rectangle = BGR(rectangle)

        start = 0

        for percent, colour in colours:
            #print(colour, f'{round((percent * 100), 5)} %')

            end = start + (percent * 300)

            cv2.rectangle(rectangle.image, (int(start), 0), (int(end), 50), colour.astype("uint8").tolist(), -1)

            start = end

        #rectangle.show()

    def identify_glare_clusters(self, clusters):

        hsv_colours = []

        for colour in clusters.cluster_centers_:

            hsv_colour = Colour().rgb_to_hsv(colour[2], colour[1], colour[0])

            hsv_colours.append(hsv_colour)

        v_values = [hsv_colour[2] for hsv_colour in hsv_colours]

        if v_values:
            mean_v_value = np.mean(v_values)
        else:
            mean_v_value = None

        glare_clusters = []

        for v_value in v_values:
            if v_value > mean_v_value:
                glare_index = v_values.index(v_value)
                glare_clusters.append(glare_index)

        return glare_clusters

    def remove_clusters(self, cluster, glare_clusters):
        cluster_labels = cluster.labels_

        cluster_labels = cluster_labels.reshape(self.image.height(), self.image.width())

        for row in range(cluster_labels.shape[0]):
            for column in range(cluster_labels.shape[1]):
                if cluster_labels[row][column] in glare_clusters:
                    self.image.image[row][column] = 0

        #self.image.show()

        return self

    def find_colour_clusters(self):

        # Load image and convert to a data of pixels

        image_data = self.image.image.reshape(self.image.height() * self.image.width(), 3)

        # Find and display most dominant colors
        clusters = KMeans(n_clusters=10).fit(image_data)

        #self.show_colour_clusters(clusters)

        return clusters

    def mask(self):

        hsv_image = HSV(self.image.image, 'BGR')

        colour_mask = hsv_image.mask(HSVRange([0, 255], [0, 255], [1, 255]))

        greyscale_mask_image = Greyscale(colour_mask, 'HSV')

        return greyscale_mask_image

    def locate(self):

        self.image = BGR(self.image.image).blur(round(self.image.width() * 10), 1)

        #self.image.show()

        clusters = self.find_colour_clusters()

        glare_clusters = self.identify_glare_clusters(clusters)

        self.remove_clusters(clusters, glare_clusters)

        return self.mask()
