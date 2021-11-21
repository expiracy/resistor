import cv2

from detection.Image import Image


# Class initiates with an image and inherits from Image. Is responsible for any annotations on the image.
class Annotation(Image):
    def __init__(self, image):
        super().__init__(image)

    # Draws a circle on a certain radius at a certain point on an image.
    def draw_circle(self, x, y, radius, thickness=2):
        self.image = cv2.circle(self.image, (x, y), radius=radius, color=(255, 255, 255), thickness=thickness)

        return self

    # Draws a rectangle of a certain width and height at a certain point on an image.
    def draw_rectangle(self, x, y, width, height, thickness=2):
        self.image = cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 255, 0), thickness)

        return self

    # Draws the contours on an image.
    def draw_contours(self, contours=None):
        for contour in contours:
            self.image = cv2.drawContours(self.image, [contour], 0, (255, 255, 255), cv2.FILLED)

        return self

    # Draws hough lines onto an image.
    def draw_hough_lines(self, lines):
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(self.image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return self

