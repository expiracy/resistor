import cv2
import numpy

from detection.Colors import Colors
from detection.Contours import Contours
from detection.Image import Image
from detection.Resistor import Resistor


class Detector:

    @classmethod
    def create(cls):
        return Detector()

    def __init__(self):
        self.image = Image.create()
        self.resistor = Resistor.create()
        self.colors = None

    def scan(self, x, y):

        height = self.image.height()

        size = 32

        angle = 0

        #offset = int(y - size / 2)
        offset = 0
        while True:

            # self.image = self.image.rotate(angle, (x, offset))

            section = self.image.rows(offset, size)

            key = section.show()

            if key == ord('4'):
                angle = angle + 1

            if key == ord('6'):
                angle = angle - 1

            if key == ord('8'):
                offset = offset - 10 if offset > 10 else 0

            if key == ord('2'):
                offset = offset + 10 if offset < height - 10 else height - 10

            if key == 13:
                key = self.process_section(section)

            if key == ord('+'):
                self.image = self.image.brighten(1.1)

            if key == ord('-'):
                self.image = self.image.brighten(0.9)

            if key == ord('>'):
                self.image = self.image.recolor(1)

            if key == ord('<'):
                self.image = self.image.recolor(-1)

            if key == 27:
                return key

        return 27


    def process_section(self, image):

        adjusted_image = image.invert_light()

        blurred_image = adjusted_image.blur()

        monochrome_image = blurred_image.monochrome(inverted=True)

        contours = Contours.create().scan(monochrome_image).select(8).boxes()

        contour_image = contours.draw(image)

        self.colors = contours.colors(image)

        Colors().display(self.colors)

        # processing resistor specific parts of image
        self.resistor = image.identifyBands(self.resistor, self.colors)

        return image.showList(
            [image.bgr(), adjusted_image.bgr(), blurred_image.bgr(), monochrome_image.bgr(),
             contour_image.bgr()],
            axis=0)

    def detect(self, location, x, y):

        self.image = Image.create().load(location).resize(512, 384)

        x = x * 512 / self.image.width()
        y = y * 384 / self.image.height()

        while True:
            key = self.scan(x, y)

            if key == 27:
                break

        cv2.destroyAllWindows()

        return self.resistor


