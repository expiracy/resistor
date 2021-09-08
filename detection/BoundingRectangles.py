class BoundingRectangles:
    def __init__(self, bounding_rectangles):
        self.bounding_rectangles = bounding_rectangles
        self.x_list = self.get_x_list()
        self.y_list = self.get_y_list()
        self.widths = self.get_heights()
        self.heights = self.get_widths()

    def get_x_list(self):
        x_list = []

        for bounding_rectangle in self.bounding_rectangles:
            x_list.append(bounding_rectangle.x)

        return x_list

    def get_y_list(self):
        y_list = []

        for bounding_rectangle in self.bounding_rectangles:
            y_list.append(bounding_rectangle.y)

        return y_list

    def get_widths(self):
        width = []

        for bounding_rectangle in self.bounding_rectangles:
            width.append(bounding_rectangle.width)

        return width

    def get_heights(self):
        heights = []

        for bounding_rectangle in self.bounding_rectangles:
            heights.append(bounding_rectangle.height)

        return heights
