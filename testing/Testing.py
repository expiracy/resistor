import os

from detection.Detector import Detector


class Testing:
    def __init__(self):
        pass

    def full_test(self):
        try:
            os.getcwd()
            os.chdir('..')

            mode = int(input('MODE: '))

            if mode == 1:

                for filename in os.listdir(f'{os.getcwd()}\\testing\\images\\'):
                    if filename.endswith('JPG'):
                        print(filename)

                        resistor, image = Detector().detect(f'{os.getcwd()}\\testing\\images\\{filename}')

                        print(resistor.colours())
                        print('\n\n\n')

            else:

                filename = 'BROWN RED RED GOLD (2)' + '.JPG'

                print(f'{os.getcwd()}\\{filename}')

                resistor, image = Detector().detect(f'{os.getcwd()}\\{filename}')

                print(resistor.colours())
                print('\n\n\n')

        except Exception as error:
            print(error)


if __name__ == '__main__':
    Testing().full_test()


