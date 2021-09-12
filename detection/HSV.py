from detection.Image import Image
import cv2
import numpy as np

class HSV(Image):
    def __init__(self):
        super().__init__()
        self.h, self.s, self.v = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV))

    def mask(self, hsv_ranges):

        h_range = cv2.inRange(self.h, hsv_ranges.h_range[0], hsv_ranges.h_range[1])
        s_range = cv2.inRange(self.s, hsv_ranges.s_range[0], hsv_ranges.s_range[1])
        v_range = cv2.inRange(self.v, hsv_ranges.v_range[0], hsv_ranges.v_range[1])

        # Narrowing down the image to only show the HSV values of the desired range
        hs_mask = np.bitwise_and(h_range, s_range)
        hsv_mask = np.bitwise_and(hs_mask, v_range)

        #cv2.imshow("original", self.image)
        #cv2.imshow("image", colour_mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        bgr_image = cv2.cvtColor(hsv_mask, cv2.COLOR_GRAY2BGR)

        return Image(bgr_image)
