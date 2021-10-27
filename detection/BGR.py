from detection.Image import Image
import cv2

class BGR(Image):
    def __init__(self, image, type='BGR'):
        bgr = self.bgr_conversion(image, type)
        super().__init__(bgr)

    def blur(self, width=1, height=-1):
        height = self.height() if height < 0 else height

        self.image = cv2.blur(self.image, (width, height))

        return self

    def bilateral_filter(self):
        self.image = cv2.bilateralFilter(self.image, 5, 100, 75)

        return self

    def greyscale_to_bgr(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        return self

    def channels(self):

        height, width, channels = self.image.shape

        return channels

    # Conversion between types.
    def bgr_conversion(self, image, type):
        if type == 'BGR':
            return image

        if type == 'GREYSCALE':
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


