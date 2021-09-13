from detection.Image import Image
import cv2
import numpy as np


class Annotation(Image):
    def __init__(self, image):
        super().__init__(image)

    def circle(self, x, y, thickness=2):

        cv2.circle(self.image, (x, y), radius=0, color=(0, 0, 255), thickness=thickness)

        return self

    def rectangle(self, x, y, width, height):

        cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 255, 0), 2)

    def contours(self, contours=None):

        try:
            for contour in contours:
                cv2.drawContours(self.image, [contour], 0, (0, 0, 255), cv2.FILLED)

            return self

        except ValueError:

            print("No contours.")

            return None

    def hough_lines(self, lines, threshold=1, min_line_length=1, max_line_gap=1):

        try:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)

            return self

        except ValueError:

            print("No hough lines.")

            return None
