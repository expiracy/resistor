import cv2
import numpy as np
from sklearn.cluster import KMeans

from detection.BGR import BGR
from detection.BoundingRectangle import BoundingRectangle
from detection.Contours import Contours
from detection.Greyscale import Greyscale
from detection.HSV import HSV
from detection.HSVRange import HSVRange


class GlareRemover:
    def __init__(self, image):
        self.image = image

    # Shows the colour clusters.
    def show_colour_clusters(self, colours):

        # Create frequency rect and iterate through each clusters's color and percentage
        rectangle = np.zeros((50, 300, 3), dtype=np.uint8)

        rectangle = BGR(rectangle)

        start = 0

        for percent, colour in colours:
            # print(colour, f'{round((percent * 100), 5)} %')

            end = start + (percent * 300)

            cv2.rectangle(rectangle.image, (int(start), 0), (int(end), 50), colour.astype('uint8').tolist(), -1)

            start = end

        # rectangle.show()

    # Identifies the glare clusters based on V values.
    def identify_glare_clusters(self, clusters):

        hsv_colours = []

        for colour in clusters.cluster_centers_:
            hsv_colours.append(colour)

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

    # Change the pixels to 0 if its closest centroid identified as a glare cluster.
    def remove_clusters(self, cluster, glare_clusters):
        cluster_labels = cluster.labels_

        cluster_labels = cluster_labels.reshape(self.image.height(), self.image.width())

        for row in range(cluster_labels.shape[0]):
            for column in range(cluster_labels.shape[1]):
                if cluster_labels[row][column] in glare_clusters:
                    self.image.image[row][column] = 0

        # self.image.show()

        return self

    # Find the colour clusters.
    def find_colour_clusters(self):

        # Load image and convert to a data of pixels

        image_data = self.image.image.reshape(self.image.height() * self.image.width(), 3)

        # Find and display most dominant colors
        clusters = KMeans(n_clusters=5).fit(image_data)

        centroids = clusters.cluster_centers_

        labels = np.arange(0, len(np.unique(clusters.labels_)) + 1)

        hist, _ = np.histogram(clusters.labels_, bins=labels)
        hist = hist.astype('float')
        hist /= hist.sum()

        colours = sorted([(percent, colour) for percent, colour in zip(hist, centroids)])

        self.show_colour_clusters(colours)

        return clusters

    # Masks the image for non black values.
    def mask(self):

        hsv_image = HSV(self.image.image, 'BGR')

        colour_mask = hsv_image.mask(HSVRange([0, 255], [0, 255], [1, 255]))

        greyscale_mask_image = Greyscale(colour_mask, 'HSV')

        return greyscale_mask_image

    # Removes the glare from the image by taking the biggest region.
    def remove_glare_from_image(self, glare_mask, image):
        image = image.mask(glare_mask.image)

        contours, _ = Greyscale(image.image, 'BGR').find_contours()

        sorted_contours = Contours(contours).sort()

        largest_contour = sorted_contours[len(sorted_contours) - 1]

        bounding_rectangle = BoundingRectangle(largest_contour)

        no_glare_image = image.region(bounding_rectangle.x, bounding_rectangle.y, bounding_rectangle.width,
                                      bounding_rectangle.height)

        return no_glare_image

    # Runs the functions within the glare remover.
    def main(self):

        try:
            original_image = self.image.clone()

            self.image = BGR(self.image.image).blur(round(self.image.width() * 10), 1)
            self.image = HSV(self.image.image, 'BGR')

            # self.image.show()

            clusters = self.find_colour_clusters()

            glare_clusters = self.identify_glare_clusters(clusters)

            self.remove_clusters(clusters, glare_clusters)

            glare_mask = self.mask()

            no_glare_image = self.remove_glare_from_image(glare_mask, original_image)

            return no_glare_image

        except Exception as E:
            print('Error with Glare.')
            print(E)
