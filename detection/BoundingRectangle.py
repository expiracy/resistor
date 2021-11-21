import cv2


# Initiates with a contour, creates a bounding rectangles and encapsulates the attributes.
class BoundingRectangle:
    def __init__(self, contour):
        self.x, self.y, self.width, self.height = cv2.boundingRect(contour)
