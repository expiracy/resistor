import cv2
import uuid
import os

from detection.Greyscale import Greyscale

class Image2:
    def __init__(self, image=None):
        self.image = image

    def clone(self):
        return Image2(self.image)

    def load(self, location):

        self.image = cv2.imread(location)

        return self

    def width(self):

        height, width, channels = self.image.shape

        return width

    def height(self):

        height, width, channels = self.image.shape

        return height

    def channels(self):

        height, width, channels = self.image.shape

        return channels

    def resize(self, width, height):

        return cv2.resize(self.image, (width, height))

    def region(self, x, y, width, height):

        return self.image[y:y + height, x:x + width]

    def show(self):

        cv2.imshow("Image", self.image)
        cv2.setMouseCallback("Image", self.mouse)

        return cv2.waitKey(0) & 0xff

    def mouse(self, event, x, y, flags, parameters):

        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            color = hsv_image[y][x]

            print(color)

    def save(self):

        id = uuid.uuid1()
        filename = str(id.int)

        save_file = f'{os.path.abspath(os.curdir)}\\detection\\resistorImages\\{filename}.jpg'

        if not cv2.imwrite(f'{save_file}', self.image):
            raise Exception("Could not write image.")

        return save_file

if __name__ == '__main__':
    image = Image2().load('C:\\Users\\expiracy\\PycharmProjects\\resistor\\images\\BROWN BLACK BROWN GOLD.JPG')

    greyscale_image = Greyscale().show()