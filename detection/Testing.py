import os
from detection.Detector import Detector

class Testing:
    def __init__(self):
        pass

    def test(self):
        os.getcwd()
        os.chdir("../images")

        for filename in os.listdir():

            print(filename)

            if filename.endswith('JPG'):
                resistor = Detector().detect(f'{os.curdir}\\{filename}')
                # compare to list


