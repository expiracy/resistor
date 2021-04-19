import cv2
import numpy

from detection.Colors import Colors
from detection.Image import Image

class Contours:

    @classmethod
    def create(cls, contours=[]):
        return Contours(contours)

    def __init__(self, contours=[]):
        self.contours = contours
        return

    def contours(self):
        return self.contours

    def clone(self):
        return Contours(self.image, self.contours)

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

        return Contours(boxes)

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

        return Contours(self.contours[start:end])

    def draw(self, image):

        bgr_image = image.bgr().copy()

        for index, contour in enumerate(self.contours):
            x, y, w, h = cv2.boundingRect(contour)

            region = image.region(x, y, w, h)

            bgr = region.color()

            cv2.rectangle(bgr_image, (x, y), (x + w, y + h), bgr, -1)

        return Image(bgr_image)

