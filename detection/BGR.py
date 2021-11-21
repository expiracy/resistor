import cv2

from detection.Image import Image


# Initiates with an image and inherits from Image. Is responsible for performing functions that work on BGR images.
class BGR(Image):
    def __init__(self, image, type='BGR'):
        bgr = self.bgr_conversion(image, type)
        super().__init__(bgr)

    # Blurs the image based on the input height and width.
    def blur(self, width=1, height=-1):
        height = self.height() if height < 0 else height

        self.image = cv2.blur(self.image, (width, height))

        return self

    # Applies a bilateral filter.
    def bilateral_filter(self):
        self.image = cv2.bilateralFilter(self.image, 5, 100, 75)

        return self

    # Conversion between types.
    def bgr_conversion(self, image, type):
        if type == 'BGR':
            return image

        if type == 'GREYSCALE':
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        if type == 'HSV':
            return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
