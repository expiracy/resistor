from detection.Image import Image
import cv2


class Monochrome(Image):
    def __init__(self):
        super().__init__()
        self.monochrome = self.monochrome()

    def monochrome(self, inverted=False, block_size=51, C=21):

        cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        thresholding = cv2.THRESH_BINARY if not inverted else cv2.THRESH_BINARY_INV

        monochrome_image = cv2.adaptiveThreshold(greyscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, thresholding,
                                                 block_size, C)

        bgr_image = cv2.cvtColor(monochrome_image, cv2.COLOR_GRAY2BGR)

