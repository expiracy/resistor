import cv2 as cv2
import numpy
import numpy as np

import os
import glob


from detection.Colours import Colours
from detection.Image import Image
from detection.ResistorBand import ResistorBand
from detection.Resistor import Resistor

class BoundingRectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class BandLocator:

    def __init__(self, image):
        self.image = image
        self.bounding_rectangles = []
        self.band_colours = []


    def scan(self, image):

        greyscale_image = cv2.cvtColor(image.bgr(), cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(greyscale_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        self.contours = sorted(contours, key=cv2.contourArea, reverse=True)


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

    def colours(self, no_glare_image, rectangles):

        matcher = Colours.create()

        colours = []

        for index in range(len(rectangles)):

            # width = int(bounding_rectangles[index].width / 2)
            # x = int(bounding_rectangles[index].x + bounding_rectangles[index].width)

            region = no_glare_image.region(rectangles[index].x, rectangles[index].y, rectangles[index].width, rectangles[index].height)

            brg = region.colour()

            print(str(brg))

            colour = matcher.find(brg)

            colours.append(colour)

        return colours

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

    def remove_outlier_rectangles(self, rectangles):

        areas = []

        for index in range(len(rectangles)):

            areas.append(rectangles[index].width * rectangles[index].height)

        mean = np.mean(areas)

        lower_bound = mean - (mean * 0.6)

        outliers = []

        # write about different outlier algorithms tried

        for index in range(len(areas)):

            if areas[index] < lower_bound:

                outliers.append(rectangles[index])

        for outlier in outliers:

            rectangles.remove(outlier)

        return rectangles

    def bounding_rectangle(self, contours):

        bounding_rectangles = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            bounding_rectangle = BoundingRectangle(x, y, w, h)

            bounding_rectangles.append(bounding_rectangle)

        #bounding_rectangles = self.remove_outlier_rectangles(bounding_rectangles)

        return bounding_rectangles

    def trim_image(self):

        image = self.image.region(round(self.image.width() * 0.04), 0, round(self.image.width() * 0.92), self.image.height() * 2)

        return image

    def locate(self):

        trimmed_image = self.trim_image()

        resized_image = trimmed_image.resize(trimmed_image.width(), trimmed_image.height() * 5)

        blurred_image = resized_image.blur(1, round(resized_image.height()))

        blurred_image.show()

        colours = ['BLACK', 'BROWN', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GREY', 'WHITE', 'GOLD', 'SILVER']

        resistor_bands = []

        for colour in colours:
            resistor_band = blurred_image.hsv_mask(colour)

            if resistor_band is not None:
                resistor_bands.append(resistor_band)

        Resistor(resistor_bands).main()





    '''
    def locate(self):

        trimmed_image = self.trim_image(self.image)

        resized_image = trimmed_image.resize(trimmed_image.width(), trimmed_image.height() * 5)

        no_glare_image = resized_image.remove_glare()

        b, g, r = cv2.split(resized_image.image)
        b = cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)

        b_image = Image(b)
        b_image.show()

        blurred_image = b_image.blur(1, round(resized_image.height()*2))
        blurred_image.show()

        monochrome_image = blurred_image.monochrome(inverted=True, block_size=61, C=4)
        monochrome_image.show()

        #closing = cv2.morphologyEx(monochrome_image.image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (round(monochrome_image.width()*0.03), round(monochrome_image.height()*0.03))))
        #closing = cv2.erode(monochrome_image.image, np.ones((4, 4), np.uint8), 5)


        #closing = Image(closing)
        #cv2.imshow("monochrome", monochrome_image.image)

        #cv2.waitKey(0)

        contours, _ = monochrome_image.contours()

        band_rectangles = self.bounding_rectangle(contours)

        #image = self.band_colours(no_glare_image)

        colours = self.colours(no_glare_image, band_rectangles)

        resized_image.show()
    '''


if __name__ == "__main__":

    directory = os.path.abspath(os.curdir)
    ''''
    folder = f'{directory}\\resistorImages'

    for filename in os.listdir(folder):
        if filename.endswith('jpg'):
            resistor_image = cv2.imread(f'{folder}\\{filename}')
            
    '''
    resistor_image = cv2.imread('C:\\Users\\expiracy\\PycharmProjects\\resistor\detection\\resistorImages\\269661054352669044576758484705730405017.jpg')
    resistor_image = Image(resistor_image)

    BandLocator(resistor_image).locate()



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


