from detection.ResistorBand import ResistorBand


# An encapsulation class that initiates with colour, bounding rectangle and hsv variance and inherits from ResistorBand.
class SliceBand(ResistorBand):
    def __init__(self, colour, bounding_rectangle, hsv_variance=None):
        super().__init__(colour)
        self.bounding_rectangle = bounding_rectangle
        self.hsv_variance = hsv_variance

    def __str__(self):
        return f"{self.colour.name}, ({self.bounding_rectangle.x}, {self.bounding_rectangle.y}, " \
               f"{self.bounding_rectangle.width}, {self.bounding_rectangle.height}), {self.hsv_variance}"

    def x_low(self):
        return self.bounding_rectangle.x

    def x_high(self):
        return self.bounding_rectangle.x + self.bounding_rectangle.width

    def x_centre(self):
        return self.bounding_rectangle.x + self.bounding_rectangle.width / 2

    def has_overlap(self, other):
        if other.x_low() - 1 <= self.x_low() <= other.x_high() + 1:
            return True

        if other.x_low() - 1 <= self.x_high() <= other.x_high() + 1:
            return True

        if self.x_low() - 1 <= other.x_low() <= self.x_high() + 1:
            return True

        if self.x_low() - 1 <= other.x_high() <= self.x_high() + 1:
            return True

        return False

    def overlaps_size(self, other):
        low = max(self.x_low(), other.x_low())

        high = min(self.x_high(), other.x_high())

        result = high - low

        if result < 0:
            return 0

        return result

    def biggest_width(self, other):
        return max(self.bounding_rectangle.width, other.bounding_rectangle.width)

    def overlap_amount(self, other):
        overlap = self.overlaps_size(other)

        width = self.biggest_width(other)

        return overlap / width

    def count_overlaps(self, slice_bands):
        result = 0

        for slice_band in slice_bands:
            if self.overlap_amount(slice_band) > 0:
                result = result + 1

        return result

    def has_any_overlaps(self, slice_bands):
        for slice_band in slice_bands:

            if self is slice_band:
                continue

            if self.has_overlap(slice_band):
                return True

        return False
