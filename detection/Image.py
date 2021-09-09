import cv2
import numpy as np
import os
import uuid

from detection.Colours import Colours

class Image:

    @classmethod
    def create(cls, image=None):
        return Image(image)

    def __init__(self, image=None):
        self.image = image
        return

    def clone(self):
        return Image(self.image)

    def load(self, location):
        self.image = cv2.imread(location)
        return self

    def bgr(self):
        return self.image

    def hsv(self):
        h, s, v = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV))

        return h, s, v

    def width(self):
        height, width, channels = self.image.shape
        return width

    def height(self):
        height, width, channels = self.image.shape
        return height

    def channels(self):
        height, width, channels = self.image.shape
        return channels

    def rotate(self, angle, center=None, scale=1.0):
        (height, width) = self.image.shape[:2]

        if center is None:
            center = (width / 2, height / 2)

        matrix = cv2.getRotationMatrix2D(center, angle, scale)

        abs_cos = abs(matrix[0, 0])
        abs_sin = abs(matrix[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        matrix[0, 2] += bound_w / 2 - center[0]
        matrix[1, 2] += bound_h / 2 - center[1]

        rotated = cv2.warpAffine(self.image, matrix, (bound_w, bound_h))

        return Image(rotated)

    def resize(self, width, height):

        bgr_image = cv2.resize(self.image, (width, height))

        return Image(bgr_image)

    def region(self, x, y, width, height):

        section = self.image[y:y + height, x:x + width]

        return Image(section)

    def rows(self, offset, count):

        return self.region(0, offset, self.width(), count)

    def invert_light(self):

        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        mask = (h >= 20) & (h <= 40)
        h[mask] = 180 - h[mask]

        mask = (v > 200) & (s < 50)
        v[mask] = 255 - v[mask]

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        cv2.imshow("bgr", bgr_image)

        return Image(bgr_image)
    '''
    def colour(self):

        avg_color_per_row = np.average(self.image, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)

        return int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
    '''

    def blur(self, width=1, height=-1):

        height = self.height() if height < 0 else height

        blurred_image = cv2.blur(self.image, (width, height))
        #blurred_image = cv2.bilateralFilter(blurred_image, 2, 100, 100)

        return Image(blurred_image)

    def bilateral_filter(self):
        blurred_image = cv2.bilateralFilter(self.image, 10, 100, 1000, 1000)

        return Image(blurred_image)


    def monochrome(self, inverted=False, block_size=51, C=21):

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        monochrome_image = cv2.adaptiveThreshold(greyscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding, block_size, C)

        bgr_image = cv2.cvtColor(monochrome_image, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def recolour(self, shift=0):

        h, s, v = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV))

        h = ((h.astype('int16') + shift) % 180).astype('uint8')

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        return Image(bgr_image)

    def brighten(self, gamma=1.0):

        table = np.array([((i / 255.0) ** (1 / gamma)) * 255
                             for i in np.arange(0, 256)]).astype('uint8')

        bgr_image = cv2.LUT(self.image, table)

        return Image(bgr_image)

    def show(self):

        cv2.imshow("Image", self.image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def show_list(self, images, axis):

        display_image = np.concatenate(images, axis=axis)

        cv2.imshow("Image", display_image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            color = hsv_image[y][x]

            print(color)

    def background(self, size):
        width = self.width()
        background_color = self.image[int(size / 2), width - 1]
        print(f"background colour: {background_color}")

        return background_color

    # method to identify the resistor colours from the identified colours
    def bands(self, resistor, colours):
        resistor.amount = 6
        resistor.colours = colours

        return resistor

    def canny(self, threshold_1=50, threshold_2=50, aperture_size=3):

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        canny_image = cv2.Canny(greyscale_image, threshold_1, threshold_2, aperture_size)

        bgr_image = cv2.cvtColor(canny_image, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def hough_lines(self, edges, threshold=1, min_line_length=1, max_line_gap=1):

        edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

        lines = cv2.HoughLinesP(edges, 100, np.pi/180, threshold, min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                #cv2.circle(self.image, (x1, y1), radius=0, color=(0, 0, 255), thickness=10)
                #cv2.circle(self.image, (x2, y2), radius=0, color=(0, 0, 255), thickness=10)

        return self, lines

    def greyscale(self):

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        bgr_image = cv2.cvtColor(greyscale_image, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def draw_circle(self, x, y, thickness=10):
        image_with_plot = cv2.circle(self.image, (x, y), radius=0, color=(0, 0, 255), thickness=thickness)

        return Image(image_with_plot)

    def draw_rectangle(self, x, y, width, height):

        image_with_rectangle = cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        return image_with_rectangle

    def draw_contours(self, contours):

        for contour in contours:
            contour_image = cv2.drawContours(self.image, [contour], 0, (0, 0, 255), cv2.FILLED)

        return Image(contour_image)

    def contours(self):

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(greyscale_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        return contours, hierarchy

    def remove_glare(self):

        h, s, v = self.hsv()

        non_saturated = s < 180  # Find all pixels that are not very saturated

        disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        non_saturated = cv2.erode(non_saturated.astype(np.uint8), disk)

        v2 = v.copy()
        v2[non_saturated == 0] = 0

        glare = v2 > 200  # filter out very bright pixels.
        # Slightly increase the area for each pixel
        glare = cv2.dilate(glare.astype(np.uint8), disk, iterations=2)

        no_glare_image = cv2.inpaint(self.image, glare, 5, cv2.INPAINT_NS)

        return Image(no_glare_image)

    def denoise(self):

        denoised_image = cv2.fastNlMeansDenoisingColored(self.image, None, 10, 10, 7, 21)

        return Image(denoised_image)

    def save(self):

        id = uuid.uuid1()
        filename = str(id.int)

        save_file = f'{os.path.abspath(os.curdir)}\\resistor\\detection\\resistorImages\\{filename}.jpg'

        print(save_file)

        if not cv2.imwrite(f'{save_file}', self.image):
            raise Exception("Could not write image.")

        return save_file

    def erode(self):

        element = cv2.getStructuringElement(cv2.MORPH_ERODE, (9, 9), (3, 3))
        eroded_image = cv2.erode(self.image, element, iterations=2)

        return Image(eroded_image)

    def monochrome_mask(self):
        pass
        #self.show()
        #monochrome_image = self.monochrome(inverted=True, block_size=151, C=1)
        #monochrome_image.show()

        #get contours for monochrome mask then compare to hsv mask


    def hsv_mask(self, hsv_ranges):

        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        h_range = cv2.inRange(h, hsv_ranges.h_range[0], hsv_ranges.h_range[1])
        s_range = cv2.inRange(s, hsv_ranges.s_range[0], hsv_ranges.s_range[1])
        v_range = cv2.inRange(v, hsv_ranges.v_range[0], hsv_ranges.v_range[1])

        # Narrowing down the image to only show the HSV values of the desired range
        mask = np.bitwise_and(h_range, s_range)
        colour_mask = np.bitwise_and(mask, v_range)

        #cv2.imshow("original", self.image)
        #cv2.imshow("image", colour_mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        bgr_image = cv2.cvtColor(colour_mask, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def count_non_zero_pixels(self):
        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        non_zero_pixels = cv2.countNonZero(greyscale_image)

        return non_zero_pixels












