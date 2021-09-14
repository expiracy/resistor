from detection.Image2 import Image2
import cv2

class BGR(Image2):
    def __init__(self, image):
        bgr = bgr(image)
        super().__init__(image)

    def blur(self, width=1, height=-1):
        height = self.height() if height < 0 else height

        self.image = cv2.blur(self.image, (width, height))

        return self

    def greyscale_to_bgr(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        return self

    def channels(self):

        height, width, channels = self.image.shape

        return channels

