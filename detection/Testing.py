import os
from detection.Detector import Detector

class Testing:
    def __init__(self):
        pass

    def test(self):
        os.getcwd()
        os.chdir("../images")

        for filename in os.listdir():

            print(f'\n{filename}')

            colour = []

            resistor = Detector().detect(f'{os.curdir}\\{filename}')
            # compare to data

            filename = filename.split()

            if not filename[len(filename) - 1].isalpha():
                filename.remove(filename[len(filename) - 1])

            detected_colours = [colour for colour in resistor.colours() if colour != 'NONE']

            correct_colours = []

            for index in range(len(detected_colours)):
                if detected_colours[index] == filename[index]:
                    correct_colours.append(True)

            print(f'DETECTED: {detected_colours}')
            print(f'EXPECTED: {filename}')
            print(f'CORRECT: {correct_colours}')



if __name__ == '__main__':
    Testing().test()


