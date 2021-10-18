import os
from detection.Detector import Detector
from detection.BandFinder import BandFinder
from detection.Image import Image
from detection.BGR import BGR
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
                    big_image = image.clone().resize(3 * image.width(), 3 * image.height())
                    big_image = BGR(big_image.image).blur(1, big_image.height() * 2)
                    big_image.show()
                    print(resistor.colours())
                    print('\n\n\n')

        else:

            filename = 'RED RED BROWN GOLD (2)' + '.JPG'

            print(f'{os.getcwd()}\\{filename}')

            resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')

            image.show()
            print(resistor.find_bands)
            print('\n\n\n')


if __name__ == '__main__':
    Testing().full_test()


