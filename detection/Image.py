import cv2
import numpy


class Image:

    @classmethod
    def create(cls, bgr_image=None):
        return Image(bgr_image)

    def __init__(self, bgr_image=None):
        self.bgr_image = bgr_image
        return

    def clone(self):
        return Image(self.bgr_image)

    def load(self, location):
        self.bgr_image = cv2.imread(location)
        return self

    def bgr(self):
        return self.bgr_image

    def width(self):
        height, width, channels = self.bgr_image.shape
        return width

    def height(self):
        height, width, channels = self.bgr_image.shape
        return height

    def channels(self):
        height, width, channels = self.bgr_image.shape
        return channels

    def rotate(self, angle, center=None, scale=1.0):
        (height, width) = self.bgr_image.shape[:2]

        if center is None:
            center = (width / 2, height / 2)

        matrix = cv2.getRotationMatrix2D(center, angle, scale)

        abs_cos = abs(matrix[0, 0])
        abs_sin = abs(matrix[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        matrix[0, 2] += bound_w / 2 - center[0]
        matrix[1, 2] += bound_h / 2 - center[1]

        rotated = cv2.warpAffine(self.bgr_image, matrix, (bound_w, bound_h))

        return Image(rotated)

    def resize(self, width, height):

        bgr_image = cv2.resize(self.bgr_image, (width, height))

        return Image(bgr_image)

    def region(self, x, y, width, height):

        section = self.bgr_image[y:y + height, x:x + width]

        return Image(section)

    def rows(self, offset, count):

        return self.region(0, offset, self.width(), count)

    def invert_light(self):

        hsv_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        mask = (h >= 20) & (h <= 40)
        h[mask] = 180 - h[mask]

        mask = (v > 200) & (s < 50)
        v[mask] = 255 - v[mask]

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        return Image(bgr_image)

    def color(self):

        avg_color_per_row = numpy.average(self.bgr_image, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)

        return int(avg_color[0]), int(avg_color[1]), int(avg_color[2])

    def blur(self, width=1, height=-1):

        height = self.height() if height < 0 else height

        blurred_image = cv2.blur(self.bgr_image, (width, height))
        blurred_image = cv2.bilateralFilter(blurred_image, 5, 75, 75)

        return Image(blurred_image)

    def monochrome(self, inverted=False):

        height, width, channels = self.bgr_image.shape

        greyscale_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2GRAY)

        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        monochrome_image = cv2.adaptiveThreshold(
            greyscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding, (height * 2) + 1, 0)

        bgr_image = cv2.cvtColor(monochrome_image, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def recolor(self, shift=0):

        hsv_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        h = ((h.astype('int16') + shift) % 180).astype('uint8')

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        return Image(bgr_image)

    def brighten(self, gamma=1.0):

        table = numpy.array([((i / 255.0) ** (1 / gamma)) * 255
                             for i in numpy.arange(0, 256)]).astype('uint8')

        bgr_image = cv2.LUT(self.bgr_image, table)

        return Image(bgr_image)

    def show(self):

        cv2.imshow("Image", self.bgr_image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def showList(self, images, axis):

        display_image = numpy.concatenate(images, axis=axis)

        cv2.imshow("Image", display_image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            # hsv_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HSV)

            color = self.bgr_image[y][x]

            print(color)

    # method to identify the resistor bands from the identified colours
    def identifyBands(self, resistor, colors):

        resistor.type = 6
        resistor.bands = colors

        return resistor


