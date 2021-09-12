from detection.Image import Image
import cv2
import numpy as np

class Greyscale(Image):
    def __init__(self):
        super().__init__()
        self.greyscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def canny(self, threshold_1=50, threshold_2=50, aperture_size=3):

        canny_image = cv2.Canny(self.greyscale_image, threshold_1, threshold_2, aperture_size)

        return canny_image

    def hough_lines(self, edges, threshold=1, min_line_length=1, max_line_gap=1):

        lines = cv2.HoughLinesP(edges, 100, np.pi/180, threshold, min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                #cv2.circle(self.image, (x1, y1), radius=0, color=(0, 0, 255), thickness=10)
                #cv2.circle(self.image, (x2, y2), radius=0, color=(0, 0, 255), thickness=10)

        return self, lines

    def to_bgr(self):

        return cv2.cvtColor(self.greyscale_image, cv2.COLOR_GRAY2BGR)