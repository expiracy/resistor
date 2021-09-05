import cv2

class BoundingRectangle:
    def __init__(self, contour):
        self.x, self.y, self.width, self.height = cv2.boundingRect(contour)






