from detection.Image import Image
import cv2

class RGB(Image):
    def __init__(self, image, type='BGR'):
        bgr = self.rgb_conversion(image, type)
        super().__init__(bgr)

    def rgb_conversion(self, image, type):
        if type == 'BGR':
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if type == 'RGB':
            return image
