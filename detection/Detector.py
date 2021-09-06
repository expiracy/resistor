import cv2
import numpy

from detection.ResistorLocator import ResistorLocator
from detection.BandLocator import BandLocator
from detection.Image import Image
from detection.Resistor import Resistor


class Detector:

    @classmethod
    def create(cls):
        return Detector()

    def __init__(self):
        self.image = Image.create()
        self.colors = None
    '''
    def scan(self, x, y):

        print(f"x: {x}, y: {y}")

        height = self.image.height()

        print(f"height {height}")

        size = 32

        angle = 0

        # offset = int(y - size / 2)
        offset = 0

        print(f"offset {offset}")

        while True:

            # self.image = self.image.rotate(angle, (x, offset))

            section = self.image.rows(offset, size)

            key = section.show()

            if key == ord('a'):
                angle += 10

            if key == ord('d'):
                angle -= 10

            if key == ord('w'):
                offset -= 10 if offset > 10 else 0

            if key == ord('s'):
                offset += 10 if offset < height - 10 else height - 10

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

        # background_color = image.background(size)

        # start and end points of select to ignore solid background
        contours = BandLocator.create().scan(monochrome_image).select(7, 1).boxes()

        contour_image = contours.draw(image)

        self.colors = contours.colors(image)

        Colors().display(self.colors)

        # processing resistor specific parts of image
        self.resistor = image.colours(self.resistor, self.colors)
        self.resistor.identify_type(self.colors)
        self.resistor.bands_for_type()

        return image.show_list(
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
    '''
    def detect(self, location):
        self.image = Image.create().load(location)

        self.image = ResistorLocator(self.image).locate()

        resistor_bands = BandLocator(self.image).locate()

        resistor = Resistor(resistor_bands).main()

        return resistor




