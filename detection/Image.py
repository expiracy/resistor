import cv2
import uuid
import os
import numpy as np
import base64


class Image:
    def __init__(self, image=None):
        self.image = image

    # Returns a copy of the image.
    def clone(self):
        return Image(self.image)

    # Loads an image at a specified location.
    def load(self, location):
        self.image = cv2.imread(location)

        return self

    # Returns the width of the image.
    def width(self):
        return self.image.shape[1]

    # Returns the height of the image.
    def height(self):
        return self.image.shape[0]

    # Resizes the image according to the specified width and height.
    def resize(self, width, height):
        self.image = cv2.resize(self.image, (width, height))

        return self

    # Returns a region of an image based on an offset and a size.
    def region(self, x, y, width, height):
        self.image = self.image[y:y + height, x:x + width]

        return self

    # Shows an image and returns colour values for clicked pixels.
    def show(self):
        try:
            cv2.destroyWindow('Image')

        except:
            print('Image window not open.')

        cv2.imshow('Image', self.image)
        cv2.setMouseCallback('Image', self.mouse)

        return cv2.waitKey(0) & 0xff

    # Handles mouse events.
    def mouse(self, event, x, y, flags, parameters):
        try:
            if event == cv2.EVENT_LBUTTONDOWN:
                hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

                color = hsv_image[y][x]

                print(color)

        except Exception as E:
            print('Clicked outside image.')
            print(E)

    # Saves an image with a random name.
    def save(self):
        filename = str(uuid.uuid1().int)

        absolute_file_path = f'{os.path.abspath(os.curdir)}\\resistorImages\\{filename}.jpg'

        if not cv2.imwrite(f'{absolute_file_path}', self.image):
            raise Exception('Could not write image.')

        return absolute_file_path

    # Warps the perspective of the image based on a matrix, width and height.
    def warp_perspective(self, matrix, width, height):
        self.image = cv2.warpPerspective(self.image, matrix, (width, height))

        return self

    # Erodes the image for a certain amount of iterations.
    def erode(self, iterations):
        element = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3), (1, 1))
        self.image = cv2.erode(self.image, element, iterations=iterations)

        return self

    # Returns the slices of an image.
    def slices(self, slice_height):
        height = self.height()

        slice_amount = height // slice_height

        image_slices = []

        for slice_number in range(slice_amount):
            x = 0
            y = slice_number * slice_height

            image_slice = self.clone().region(x, y, self.width(), slice_height)

            image_slices.append(image_slice)

        return image_slices

    # Masks an image based on an input mask.
    def mask(self, mask):
        self.image = cv2.bitwise_and(self.image, self.image, mask=mask)

        return self

    # Rotates the image 90 degrees clockwise.
    def rotate_90_clockwise(self):
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)

        return self

    # Returns the byte-stream for an image.
    def byte_stream(self):
        encoded_image, buffer = cv2.imencode('.jpg', self.image)
        byte_stream_image = base64.b64encode(buffer)

        return byte_stream_image