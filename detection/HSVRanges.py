from detection.HSVRange import HSVRange


class HSVRanges:
    def __init__(self):
        pass

    # The HSV ranges for all the resistor colours.
    def hsv_ranges(self, colour):
        h_ranges = {
            'BLACK': [0, 255],
            'BROWN': [0, 15],
            'RED': [150, 180],
            'ORANGE': [5, 15],
            'YELLOW': [20, 70],
            'GREEN': [40, 80],
            'BLUE': [90, 140],
            'VIOLET': [120, 160],
            'GREY': [0, 0],
            'WHITE': [0, 180],
            'GOLD': [10, 23],
            'SILVER': [0, 0],
        }

        s_ranges = {
            'BLACK': [0, 255],
            'BROWN': [80, 140],
            'RED': [60, 200],
            'ORANGE': [100, 180],
            'YELLOW': [100, 255],
            'GREEN': [100, 255],
            'BLUE': [150, 255],
            'VIOLET': [30, 140],
            'GREY': [0, 0],
            'WHITE': [0, 30],
            'GOLD': [70, 110],
            'SILVER': [0, 1],
        }

        v_ranges = {
            'BLACK': [0, 30],
            'BROWN': [40, 80],
            'RED': [60, 110],
            'ORANGE': [80, 140],
            'YELLOW': [100, 255],
            'GREEN': [0, 255],
            'BLUE': [0, 130],
            'VIOLET': [40, 120],
            'GREY': [40, 130],
            'WHITE': [127, 255],
            'GOLD': [20, 80],
            'SILVER': [80, 130],
        }

        return HSVRange(h_ranges[colour], s_ranges[colour], v_ranges[colour])