import cv2
import numpy

from detection.Picker import Picker


class Detector:

    def __init__(self):
        self.picker = Picker()

    def rotate(self, image, angle, center=None, scale=1.0):
        (height, width) = image.shape[:2]

        if center is None:
            center = (width / 2, height / 2)

        matrix = cv2.getRotationMatrix2D(center, angle, scale)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(matrix[0, 0])
        abs_sin = abs(matrix[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        matrix[0, 2] += bound_w / 2 - center[0]
        matrix[1, 2] += bound_h / 2 - center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated = cv2.warpAffine(image, matrix, (bound_w, bound_h))

        return rotated

    def scan(self, bgr_image, x, y):

        height, width, channels = bgr_image.shape

        size = 32

        angle = 0

        offset = int(y - size / 2)

        while True:

            image = self.rotate(bgr_image, angle, (x, offset))

            section = self.select_section(image, offset, size)

            key = self.show(section)

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

            if key == ord('c'):
                key = self.show_colorspace(section)

            if key == ord('p'):
                key = self.picker.pick(bgr_image)

            if key == ord('+'):
                bgr_image = self.adjust_brightness(bgr_image, 1.1)

            if key == ord('-'):
                bgr_image = self.adjust_brightness(bgr_image, 0.9)

            if key == ord('>'):
                bgr_image = self.adjust_hue(bgr_image, 1)

            if key == ord('<'):
                bgr_image = self.adjust_hue(bgr_image, -1)

            if key == 27:
                return key

        return 27

    def select_section(self, bgr_image, offset, size):

        height, width, channels = bgr_image.shape

        section = bgr_image[offset:offset + size, 0:width]

        return section

    def invert_yellow(self, bgr_image):

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        selection = (h > 20) & (h < 35)

        h[selection] = (180 - h[selection])

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        return bgr_image

    def monochrome(self, bgr_image):

        height, width, channels = bgr_image.shape

        greyscale_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.blur(greyscale_image, (1, height))
        blurred_image = cv2.bilateralFilter(blurred_image, 5, 75, 75)

        # threshold, threshold_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY)

        threshold_image = cv2.adaptiveThreshold(
            blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, (height * 2) + 1, 0)

        return threshold_image



    def show_colorspace(self, bgr_image):

        height, width, channels = bgr_image.shape

        blurred_image = cv2.blur(bgr_image, (1, height))
        blurred_image = cv2.blur(blurred_image, (1, height))

        hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

        red_image = self.mask_image(hsv_image, self.red_mask(hsv_image))
        orange_image = self.mask_image(hsv_image, self.orange_mask(hsv_image))
        yellow_image = self.mask_image(hsv_image, self.yellow_mask(hsv_image))
        green_image = self.mask_image(hsv_image, self.green_mask(hsv_image))
        blue_image = self.mask_image(hsv_image, self.blue_mask(hsv_image))
        purple_image = self.mask_image(hsv_image, self.purple_mask(hsv_image))
        brown_image = self.mask_image(hsv_image, self.brown_mask(hsv_image))
        white_image = self.mask_image(hsv_image, self.white_mask(hsv_image))
        grey_image = self.mask_image(hsv_image, self.grey_mask(hsv_image))
        black_image = self.mask_image(cv2.bitwise_not(hsv_image), self.black_mask(hsv_image))

        display_image = numpy.concatenate([hsv_image,
                                           red_image,
                                           orange_image,
                                           yellow_image,
                                           green_image,
                                           blue_image,
                                           purple_image,
                                           brown_image,
                                           white_image,
                                           grey_image,
                                           black_image], axis=0)

        display_image = cv2.cvtColor(display_image, cv2.COLOR_HSV2BGR)

        return self.show(display_image)

    def red_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (0, 50, 50), (5, 255, 255))
        mask += cv2.inRange(hsv_image, (165, 50, 50), (179, 255, 255))
        return mask

    def orange_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (5, 100, 50), (20, 255, 255))
        return mask

    def yellow_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (20, 100, 50), (35, 255, 255))
        return mask

    def green_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (35, 50, 50), (90, 255, 255))
        return mask

    def blue_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (100, 50, 50), (130, 255, 255))
        return mask

    def purple_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (130, 50, 50), (165, 255, 255))
        return mask

    def brown_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (0, 100, 10), (15, 255, 200))
        return mask

    def white_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (0, 0, 200), (179, 255, 200))
        return mask

    def grey_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (0, 0, 50), (179, 255, 200))
        return mask

    def black_mask(self, hsv_image):
        mask = cv2.inRange(hsv_image, (0, 0, 0), (179, 255, 50))
        return mask

    def mask_image(self, hsv_image, mask):
        return cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

    def process_section(self, bgr_image):

        height, width, channels = bgr_image.shape

        greyscale_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.blur(greyscale_image, (1, height))
        blurred_image = cv2.bilateralFilter(blurred_image, 5, 75, 75)

        # threshold, threshold_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY)

        threshold_image = cv2.adaptiveThreshold(
            blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, (height * 2) + 1, 0)

        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contour_image = cv2.drawContours(greyscale_image.copy(), contours, -1, (0, 255, 0))

        monochrome_image = self.monochrome(self.invert_yellow(bgr_image))

        display_image = numpy.concatenate([greyscale_image, blurred_image, threshold_image, contour_image, monochrome_image], axis=0)

        return self.show(display_image)

    def adjust_hue(self, bgr_image, shift=0):

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        h = ((h.astype('int16') + shift) % 180).astype('uint8')

        hsv_image = cv2.merge([h, s, v])

        return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    def adjust_brightness(self, image, gamma=1.0):

        table = numpy.array([((i / 255.0) ** (1 / gamma)) * 255
                             for i in numpy.arange(0, 256)]).astype('uint8')

        return cv2.LUT(image, table)

    def detect(self, location, x, y):

        bgr_image = cv2.imread(location)

        height, width, channels = bgr_image.shape

        bgr_image = cv2.resize(bgr_image, (512, 384))

        x = x * 512 / width
        y = y * 384 / height

        while True:
            key = self.scan(bgr_image, x, y)

            if key == 27:
                break

        cv2.destroyAllWindows()

    def show(self, image):

        cv2.imshow("Image", image)

        return cv2.waitKey(0) & 0xff
