import json
import os

from detection.Detector import Detector


class Testing:
    def __init__(self):
        pass

    def full_test(self):
        try:
            os.getcwd()
            os.chdir('..')

            with open(f'{os.getcwd()}\\testing\\results\\expectedValuesImages.json') as expected_values_json:

                expected_values = json.load(expected_values_json)

            image_directory = f'{os.getcwd()}\\testing\\images\\testImages'

            correct_count = 0
            total_count = 0

            for number, filename in enumerate(os.listdir(image_directory)):
                print(f'FILE: {filename}')

                if filename.endswith('JPG'):

                    detected_values = []

                    try:
                        resistor, image = Detector().detect(f'{image_directory}\\{filename}', 4)

                        detected_values = [band for band in resistor.colours() if band is not None]

                    except Exception as error:
                        print(f'{error}')

                    print(f'DETECTED: {detected_values}, EXPECTED: {expected_values[filename]}')

                    # image.show()

                    forward_matches = 0

                    correct_values = expected_values[filename]

                    total_count += len(correct_values)

                    for value in range(len(detected_values)):
                        if detected_values[value] == correct_values[value]:
                            forward_matches += 1

                    correct_values.reverse()

                    reverse_matches = 0
                    for value in range(len(detected_values)):
                        if detected_values[value] == correct_values[value]:
                            reverse_matches += 1

                    matches = max(forward_matches, reverse_matches)

                    correct_count += matches

                    print(
                        f'CORRECT={correct_count}, TOTAL={total_count} ACCURACY: {(correct_count / total_count) * 100}%')

        except Exception as error:
            print(error)

if __name__ == '__main__':
    Testing().full_test()


