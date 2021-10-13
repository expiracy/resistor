from detection.Image import Image
import cv2
import numpy as np


class Annotation(Image):
    def __init__(self, image):
        super().__init__(image)

    def draw_circle(self, x, y, thickness=2):

        self.image = cv2.circle(self.image, (x, y), radius=0, color=(255, 255, 255), thickness=thickness)

        return self

    def draw_rectangle(self, x, y, width, height, thickness=2):

        self.image = cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 255, 0), thickness)

        return self

    def draw_contours(self, contours=None):

        for contour in contours:
            self.image = cv2.drawContours(self.image, [contour], 0, (255, 255, 255), cv2.FILLED)

        return self

    def draw_hough_lines(self, lines):

        try:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)

            return self

        except ValueError:

            print("No hough lines.")

            return None
