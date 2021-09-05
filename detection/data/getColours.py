import csv
import json

file = 'standardResistorValues2sf.csv'


def get_colours(digits):

    colour_codes = {
        '0': 'BLACK',
        '1': 'BROWN',
        '2': 'RED',
        '3': 'ORANGE',
        '4': 'YELLOW',
        '5': 'GREEN',
        '6': 'BLUE',
        '7': 'VIOLET',
        '8': 'GREY',
        '9': 'WHITE'
    }

    colours = []

    for index in range(len(digits)):
        colour = colour_codes[digits[index]]

        colours.append(colour)

    return colours


with open(file, encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    colours_list = []

    for row in csv_reader:
        for value in row:
            colours = get_colours(str(value))

            colours_list.append(colours)

out = open("standardResistorValues2sf.json", "w")
json_out_data = json.dumps(colours_list)
out.write(json_out_data)
out.close()





