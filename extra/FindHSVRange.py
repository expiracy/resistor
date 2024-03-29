import numpy as np


def find_hsv_range(values):
    mean = np.mean(values, axis=0)
    maxes = np.amax(values, axis=0)
    mins = np.amin(values, axis=0)

    medians = np.median(values, axis=0)

    print(maxes)
    print(mean)
    print(medians)
    print(mins)


black_values = [[6, 170, 30], [6, 170, 30], [6, 173, 28], [5, 177, 26], [5, 186, 26], [4, 173, 25], [5, 191, 24],
                [176, 105, 34], [176, 109, 35], [0, 117, 37], [176, 105, 39], [0, 114, 38], [178, 83, 40], [5, 148, 55],
                [6, 137, 54], [7, 142, 54], [7, 137, 54], [8, 139, 55], [8, 137, 56], [8, 137, 56], [9, 114, 47],
                [8, 125, 47], [9, 136, 45], [9, 161, 46], [9, 172, 43], [6, 154, 48], [7, 156, 49], [8, 159, 48],
                [7, 154, 38], [6, 163, 39], [7, 170, 39], [6, 174, 38], [7, 174, 38], [6, 185, 33], [7, 188, 34],
                [0, 121, 40], [4, 137, 41], [6, 157, 39], [7, 168, 38], [7, 168, 38], [7, 177, 36], [7, 174, 38]]
values = [[4, 163, 50], [5, 163, 50], [5, 167, 49], [4, 163, 50], [4, 157, 52], [5, 165, 51], [5, 165, 51],
          [4, 167, 52], [5, 167, 52], [177, 147, 78], [177, 149, 77], [178, 163, 78], [177, 182, 80], [177, 181, 83],
          [177, 178, 83], [177, 179, 84], [177, 161, 87], [177, 171, 88], [178, 181, 90], [178, 182, 91],
          [176, 157, 83], [176, 179, 84], [176, 181, 86], [177, 192, 61], [179, 199, 64], [179, 194, 67],
          [179, 194, 67], [178, 162, 82], [178, 166, 86], [178, 158, 89], [178, 157, 91], [179, 119, 79],
          [179, 143, 82], [179, 141, 87], [178, 147, 87], [178, 192, 61], [179, 203, 59], [178, 207, 59],
          [179, 188, 57], [178, 210, 63], [179, 202, 58], [178, 211, 58], [179, 208, 60], [179, 207, 53],
          [179, 207, 53], [179, 212, 65], [179, 210, 62], [178, 213, 61], [178, 207, 75], [177, 201, 75],
          [177, 209, 72], [178, 208, 71]]
values = [[11, 194, 80], [11, 197, 83], [11, 202, 87], [11, 205, 92], [11, 203, 94], [11, 201, 95], [12, 203, 94],
          [12, 156, 93], [11, 177, 98], [10, 175, 102], [10, 174, 104], [9, 166, 106], [10, 181, 110], [10, 186, 114],
          [10, 168, 117], [10, 165, 113], [11, 171, 112], [11, 172, 108], [11, 164, 106], [7, 193, 86], [9, 189, 81],
          [8, 201, 81], [8, 206, 78], [8, 207, 74], [8, 207, 74], [9, 217, 87], [8, 213, 85], [8, 217, 81],
          [8, 220, 80], [8, 200, 116], [8, 206, 114], [8, 211, 111], [8, 210, 108], [11, 177, 95], [11, 185, 98],
          [12, 194, 105], [11, 178, 106]]
values = [[17, 110, 79], [16, 115, 73], [17, 113, 68], [17, 121, 61], [16, 117, 59], [16, 121, 55], [16, 123, 52],
          [17, 126, 73], [17, 123, 52], [18, 124, 70], [18, 130, 57], [18, 132, 56], [16, 133, 50], [17, 128, 50],
          [17, 128, 50], [14, 117, 37], [13, 112, 41], [14, 113, 43], [15, 109, 47], [16, 109, 49], [15, 109, 56],
          [15, 109, 61], [15, 112, 64], [15, 102, 75], [14, 98, 73], [15, 105, 75], [15, 108, 73], [15, 92, 78],
          [18, 95, 99], [18, 93, 126], [21, 90, 142], [19, 88, 101], [17, 95, 91], [15, 96, 82], [16, 93, 71],
          [17, 95, 67], [16, 93, 66], [16, 93, 66], [13, 117, 35], [13, 113, 36], [15, 112, 80], [15, 113, 111],
          [15, 113, 68], [17, 94, 68], [16, 86, 71], [16, 96, 56], [17, 89, 57], [17, 96, 53], [13, 72, 57],
          [13, 85, 57], [14, 89, 69], [14, 84, 79], [13, 86, 86], [18, 90, 68], [19, 90, 68], [19, 89, 69],
          [19, 78, 78], [19, 87, 79], [18, 82, 106], [18, 83, 77], [19, 81, 76], [18, 83, 80], [20, 66, 93],
          [18, 82, 90], [12, 117, 48], [13, 105, 39], [13, 113, 36], [18, 125, 57], [17, 123, 56], [21, 109, 115],
          [20, 125, 110], [16, 128, 48], [15, 130, 61], [13, 142, 43], [16, 124, 99], [16, 107, 95], [17, 108, 85],
          [15, 139, 33], [17, 126, 83], [16, 133, 71], [15, 124, 66], [17, 117, 50], [20, 102, 50], [18, 127, 56],
          [17, 95, 70], [15, 95, 59], [15, 88, 58]]
find_hsv_range(values)
