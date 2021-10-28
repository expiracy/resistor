import os
from detection.Detector import Detector
from detection.SliceBandsFinder import SliceBandsFinder
from detection.Image import Image
from detection.BGR import BGR
from detection.Greyscale import Greyscale
import cv2

class Testing:
    def __init__(self):
        pass

    def full_test(self):
        try:
            os.getcwd()
            os.chdir("../images")

            mode = int(input('MODE: '))

            if mode == 1:

                for filename in os.listdir():
                    if filename.endswith('JPG'):

                        print(filename)

                        resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')
                        '''
                        big_image = image.clone().resize(3 * image.width(), 3 * image.height())
                        big_image = BGR(big_image.image).blur(1, big_image.height() * 2)
                        big_image = Greyscale(big_image.image, 'BGR').monochrome(inverted=True)
                        big_image.show()
                        '''
                        print(resistor.bands)
                        print('\n\n\n')

            else:

                filename = 'RED RED BROWN GOLD' + '.JPG'

                print(f'{os.getcwd()}\\{filename}')

                resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')

                print(resistor.bands)
                print('\n\n\n')

        except Exception as E:
            print(E)


if __name__ == '__main__':
    Testing().full_test()


