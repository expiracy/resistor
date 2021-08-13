import cv2
import numpy
from matplotlib import pyplot as plt

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

        return Image(bgr_image)

    def color(self):

        avg_color_per_row = numpy.average(self.image, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)

        return int(avg_color[0]), int(avg_color[1]), int(avg_color[2])

    def blur(self, width=1, height=-1):

        height = self.height() if height < 0 else height

        blurred_image = cv2.blur(self.image, (width, height))
        blurred_image = cv2.bilateralFilter(blurred_image, 5, 75, 75)

        return Image(blurred_image)

    def monochrome(self, inverted=False):

        height, width, channels = self.image.shape

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        monochrome_image = cv2.adaptiveThreshold(
            greyscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding, (height * 2) + 1, 0)

        bgr_image = cv2.cvtColor(monochrome_image, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)

    def recolor(self, shift=0):

        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv_image)

        h = ((h.astype('int16') + shift) % 180).astype('uint8')

        hsv_image = cv2.merge([h, s, v])

        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        return Image(bgr_image)

    def brighten(self, gamma=1.0):

        table = numpy.array([((i / 255.0) ** (1 / gamma)) * 255
                             for i in numpy.arange(0, 256)]).astype('uint8')

        bgr_image = cv2.LUT(self.image, table)

        return Image(bgr_image)

    def show(self):

        cv2.imshow("Image", self.image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def show_list(self, images, axis):

        display_image = numpy.concatenate(images, axis=axis)

        cv2.imshow("Image", display_image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            # hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            color = self.image[y][x]

            print(color)

    def background(self, size):
        width = self.width()
        background_color = self.image[int(size / 2), width - 1]
        print(f"background colour: {background_color}")
        return background_color

    # method to identify the resistor colours from the identified colours
    def bands(self, resistor, colors):
        resistor.amount = 6
        resistor.colours = colors

        return resistor

    def apply_canny(self):
        self.image = cv2.Canny(self.image, 50, 150, apertureSize=3)

        return self

    def apply_hough_lines(self, edges):
        lines = cv2.HoughLinesP(edges, 3, numpy.pi/180, 10, minLineLength=10, maxLineGap=30)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return self, lines

    def apply_greyscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        return self

    def apply_kmeans(self):
        '''
        img = self.image
        Z = img.reshape((-1, 3))
        # convert to np.float32
        Z = numpy.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 2
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        # Now convert back into uint8, and make original image
        center = numpy.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape(img.shape)
        cv2.imshow('res2', res2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Change color to RGB (from BGR)

        # Reshaping the image into a 2D array of pixels and 3 color values (RGB)
        pixel_values = image.reshape((-1, 3))
        # Convert to float type only for supporting cv2.kmean
        pixel_values = numpy.float32(pixel_values)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)  # criteria
        k = 2  # Choosing number of cluster
        retval, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        centers = numpy.uint8(centers)  # convert data into 8-bit values
        segmented_data = centers[labels.flatten()]  # Mapping labels to center points( RGB Value)
        segmented_image = segmented_data.reshape((image.shape))  # reshape data into the original image dimensions

        plt.imshow(segmented_image)

        self.image = segmented_image

        return self




