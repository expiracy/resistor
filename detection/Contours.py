import cv2

from detection.MergeSort import MergeSort


# Initiates with contours and is responsible for carrying out operations on contours.
class Contours:
    def __init__(self, contours):
        self.contours = contours

    # Finds the biggest contour from a list of contours.
    def find_biggest(self):
        try:
            sorted_contours = self.sort()

            biggest_contour = sorted_contours[len(self.contours) - 1]

            return biggest_contour

        except Exception as error:
            raise Exception(f'Error finding biggest contour, {error}')

    # Sorts contours based on their areas.
    def sort(self):
        try:
            contour_areas = []
            area_for_contour = {}

            for contour in self.contours:
                contour_area = cv2.contourArea(contour)
                contour_areas.append(contour_area)
                area_for_contour[contour_area] = contour

            contour_areas = [cv2.contourArea(contour) for contour in self.contours]

            sorted_contour_areas = MergeSort().sort(contour_areas)

            sorted_contours = []

            for sorted_contour_area in sorted_contour_areas:
                sorted_contours.append(area_for_contour[sorted_contour_area])

            return sorted_contours

        except Exception as error:
            raise Exception(f'Error sorting contours, {error}')
