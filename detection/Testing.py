import os
from detection.Detector import Detector
from detection.BandLocator import BandLocator
from detection.Image import Image

import cv2

class Testing:
    def __init__(self):
        pass

    def full_test(self):
        os.getcwd()
        os.chdir("../images")

        for filename in os.listdir():

            print(f'\n{filename}')

            colour = []

            resistor, image = Detector().detect(f'{os.curdir}\\{filename}')

            # compare to data

            filename = filename.split()

            if not filename[len(filename) - 1].isalpha():
                filename.remove(filename[len(filename) - 1])

            detected_colours = [colour for colour in resistor.colours() if colour != 'NONE']


    def test_band_locator(self):

        mode = int(input('MODE: '))

        directory = os.path.abspath(os.curdir)

        folder = f'{directory}\\resistorImages'

        if mode == 1:

            for filename in os.listdir(folder):
                if filename.endswith('jpg'):
                    print(filename)
                    resistor_image = cv2.imread(f'{folder}\\{filename}')
                    resistor_image = Image(resistor_image)

                    BandLocator(resistor_image).locate()

        else:
            filename = '252947142356269709106327066630898623129.jpg'

            resistor_image = cv2.imread(f'{folder}\\{filename}')
            resistor_image = Image(resistor_image)

            BandLocator(resistor_image).locate()


if __name__ == '__main__':
    #Testing().test_band_locator()
    Testing().full_test()


