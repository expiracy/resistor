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

        mode = int(input('MODE: '))

        if mode == 1:

            for filename in os.listdir():
                if filename.endswith('JPG'):

                    print(filename)

                    resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')

                    image.show()
                    print(resistor.bands)
                    print('\n\n\n')

        else:

            filename = 'RED RED BROWN GOLD (2)' + '.JPG'

            print(f'{os.getcwd()}\\{filename}')

            resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')

            image.show()
            print(resistor.bands)
            print('\n\n\n')


if __name__ == '__main__':
    Testing().full_test()


