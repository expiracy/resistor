import cv2 as cv2
import numpy
import numpy as np

import os
import glob
from matplotlib import pyplot
from sklearn.cluster import KMeans

from detection.Colors import Colors
from detection.Image import Image

class BandLocator:

    @classmethod
    def create(cls, contours=[]):
        return BandLocator(contours)

    def __init__(self, contours=[]):
        self.contours = contours
        return

    def get_contours(self):
        return self.contours

    def clone(self):
        return BandLocator(self.image, self.contours)

    def scan(self, image):

        greyscale_image = cv2.cvtColor(image.bgr(), cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(greyscale_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        self.contours = sorted(contours, key=cv2.contourArea, reverse=True)

        return self

    def boxes(self):

        boxes = []

        for contour in self.contours:
            x, y, w, h = cv2.boundingRect(contour)
            if x == 0:
                continue
            if y != 0:
                continue
            # Box points made with lowest x value first so sorting works later
            box = [[x, y], [x, y+h], [x+w, y+h], [x+w, y]]
            box = numpy.int0(box)
            boxes.append(box)

        # Relies on the box points being put with lowest x value first
        boxes = sorted(boxes, key=lambda point: point[0][0])

        return BandLocator(boxes)

    def colors(self, image):

        matcher = Colors.create()

        colors = []

        for contour in self.contours:
            x, y, w, h = cv2.boundingRect(contour)

            w = int(w / 2)
            x = int(x + w)

            region = image.region(x, y, w, h)

            brg = region.color()

            print(str(brg))

            color = matcher.find(brg)

            colors.append(color)

        return colors

    def select(self, end, start=0):

        return BandLocator(self.contours[start:end])

    def draw(self, image):

        bgr_image = image.bgr().copy()

        for index, contour in enumerate(self.contours):
            x, y, w, h = cv2.boundingRect(contour)

            region = image.region(x, y, w, h)

            bgr = region.color()

            cv2.rectangle(bgr_image, (x, y), (x + w, y + h), bgr, -1)

        return Image(bgr_image)

    def remove_background(self, image):
        # Load the aerial image and convert to HSV colourspace
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define lower and uppper limits of what we call "brown"
        brown_lo = np.array([74, 90, 97])
        brown_hi = np.array([106, 113, 121])

        # Mask image to only select browns
        mask = cv2.inRange(hsv, brown_lo, brown_hi)

        # Change image to red where we found brown
        image[mask > 0] = (0, 0, 255)

        cv2.imshow("epic", image)


    def locate(self, image):
        resized_image = image.resize(image.width(), image.height()*3)
        no_glare_image = resized_image.remove_glare()

        blurred_image = no_glare_image.blur(1, round(resized_image.height()/2))

        inverted_image = blurred_image.invert_light()

        canny_image = inverted_image.canny(50, 50)
        canny_image.show()

        canny_image.show()

        contours, _ = canny_image.contours()

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(resized_image.image, (x, y), (x + w, y + h), (200, 0, 0), 1)



if __name__ == "__main__":

    directory = os.path.abspath(os.curdir)

    folder = f'{directory}\\resistorImages'

    for filename in os.listdir(folder):

        band_locator = BandLocator()

        if filename.endswith('jpg'):
            resistor_image = cv2.imread(f'{folder}\\{filename}')

            band_locator.locate(Image(resistor_image))



    '''
    image = Image().load(filename)

    greyscale_image = image.greyscale()
    greyscale_image.show()

    canny = image.canny()

    canny.show()
    '''

    """
    resized_image = image.resize(image.width(), image.height()*5)

    no_glare_image = resized_image.remove_glare()
    no_glare_image.show()

    denoised_image = no_glare_image.denoise()
    denoised_image.show()


    blurred_image = no_glare_image.blur(1, round(no_glare_image.height()/1.5))

    blurred_image.show()

    greyscale_image = blurred_image.greyscale()

    canny_image = greyscale_image.canny(40, 40)
    canny_image.show()

    contours, _ = canny_image.contours()

    band_locator = BandLocator(contours)

    band_locator.remove_background(resized_image.image)

    #result_image = band_locator.draw(resized_image)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(resized_image.image, (x, y), (x + w, y + h), (200, 0, 0), 1)

    resized_image.show()
    """
    """
    h, s, v = blurred_image.hsv()
    cv2.imshow("h", h)
    cv2.imshow("s", s)
    cv2.imshow("v", v)
    cv2.waitKey(0)
    """

    """
    min_hue = 0
    min_sat = 0
    min_val = 0
    max_hue = 180
    max_sat = 75
    max_val = 100

    hsv_image = cv2.cvtColor(blurred_image.image, cv2.COLOR_BGR2HSV)

    binary_img = cv2.inRange(hsv_image, (min_hue, min_sat, min_val), (max_hue, max_sat, max_val))

    resistor_image = Image(binary_img)

    resistor_image.monochrome(True)

    closing = cv2.morphologyEx(resistor_image.image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))

    filled_in_image = Image(closing)

    filled_in_image.show()

    canny_resistor_image = filled_in_image.canny(60, 60)

    canny_resistor_image.show()
    """

    #resistor_image = cv2.bitwise_and(greyscale_image.image, mask)

    #mask_image = Image(mask)

    #mask_image.show()

    #canny_mask_image = mask_image.canny()

    #canny_mask_image.show()

    """
    corners = []

    kmeans = KMeans(
        init="random",
        n_clusters=4,
        n_init=3,
        max_iter=300,
        random_state=30
    )

    #kmeans.fit(dbscan.components_)
    kmeans.fit(corners)

    counts = numpy.zeros(len(kmeans.labels_))

    biggest = 0

    for label in kmeans.labels_:
        counts[label] = counts[label] + 1
        if counts[label] > counts[biggest]:
            biggest = label

    #for point in kmeans.cluster_centers_:
    #    cv.circle(image, (x, y), 3, (0, 0, 255), 3)

    x = int(kmeans.cluster_centers_[biggest][0])
    y = int(kmeans.cluster_centers_[biggest][1])
    cv2.circle(image.image, (x, y), 3, (255, 0, 255), 3)

    image.show()


    monochrome_image = sharpened_image.greyscale().monochrome(inverted=True)

    monochrome_image.show()

    monochrome_image = blurred_image.monochrome(inverted=True)

    # background_color = image.background(size)

    adjusted_image = image.invert_light()

    blurred_image = adjusted_image.blur()

    monochrome_image = blurred_image.monochrome(inverted=True)

    contours = BandLocator.create().scan(monochrome_image).select(7, 1).boxes()

    contour_image = contours.draw(image)

    contour_image.show()
    """


