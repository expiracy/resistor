import math
import os
import random
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

import cv2 as cv
import imutils
import numpy as np
from imutils import contours, perspective

def crop(image):

    denoised = cv.bilateralFilter(image, 15, 150, 150)
    #denoised = cv.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 14)

    edges = cv.Canny(denoised, 50, 250)

    x, y, w, h = cv.boundingRect(edges)

    x = max(0, x - 50)
    y = max(0, y - 50)
    w = w + 100
    h = h + 100

    image = image[y:y+h, x:x+w]

    return image


def locate(image):

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    features = cv.goodFeaturesToTrack(gray, 10, 0.0001, 1, blockSize=25)

    corners = []

    for feature in features:
        x = int(feature[0][0])
        y = int(feature[0][1])
        corner = (x, y)
        corners.append(corner)

    kmeans = KMeans(
        init="random",
        n_clusters=2,
        n_init=3,
        max_iter=300,
        random_state=30
    )

    #kmeans.fit(dbscan.components_)
    kmeans.fit(corners)

    counts = np.zeros(len(kmeans.labels_))

    biggest = 0

    for label in kmeans.labels_:
        counts[label] = counts[label] + 1
        if counts[label] > counts[biggest]:
            biggest = label

    #for point in kmeans.cluster_centers_:
    #    cv.circle(image, (x, y), 3, (0, 0, 255), 3)

    x = int(kmeans.cluster_centers_[biggest][0])
    y = int(kmeans.cluster_centers_[biggest][1])
    cv.circle(image, (x, y), 3, (0, 0, 255), 3)

    return (x, y), image



def sharpen(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def main(filename):

    image = cv.imread(filename)

    #image = crop(image)

    #image = sharpen(image)

    point, image = locate(image)

    cv.circle(image, (point[0], point[1]), 20, (0, 0, 255), 20)

    cv.imshow("image", image)

    cv.waitKey()

    cv.destroyAllWindows()





if __name__ == '__main__':

    os.chdir("..")

    folder = f"{os.path.abspath(os.curdir)}\\images\\"

    for filename in os.listdir(folder) :

        print(filename)

        if filename.endswith('JPG') :
            main(folder + '\\' + filename)

