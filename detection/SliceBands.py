import numpy as np


# Class for slice bands operations
class SliceBands:
    def __init__(self):
        self.slice_bands = []
        self.slice_band_groups = []

    # Outputting the slice bands nicely when printed.
    def __str__(self):
        text = ''

        for index, overlap_group in enumerate(self.groups()):
            text += f'Group {index}\n'

            for slice_band in overlap_group:
                text += '    ' + str(slice_band) + '\n'

        return text

    # Loading the slice band groups from a dictionary of slice band groups.
    def load_slice_band_groups(self, slice_band_dictionary):
        try:
            for slice_band_group in slice_band_dictionary.values():
                self.slice_band_groups.append(slice_band_group)

            return self

        except Exception as error:
            print(f'load_slice_band_groups(), {error}')

    # Returns the slice bands from the self values
    def list(self):
        return self.slice_bands

    # Returns the slice band groups from the self values.
    def groups(self):
        return self.slice_band_groups

    # Returns the amount of  slice band groups
    def get_band_group_count(self):
        return len(self.groups())

    # Adds a slice band to the slice bands and re-sorts the slice bands depending on their x centres.
    def add_band(self, slice_band):
        try:
            self.slice_bands.append(slice_band)
            self.slice_bands = sorted(self.slice_bands, key=lambda band: band.x_centre())

            self.slice_band_groups = self.insert_into_slice_band_group(self.slice_band_groups, slice_band)

            return self

        except Exception as error:
            print(f'add_band(), {error}')

    # Adds multiple slice bands to the slice bands.
    def add_bands(self, slice_bands):
        for slice_band in slice_bands:
            self.add_band(slice_band)

        return self

    # Removes a band from the slice bands.
    def remove_band(self, slice_band):
        try:
            self.slice_bands.remove(slice_band)

            for slice_band_group in self.slice_band_groups:

                if slice_band in slice_band_group:
                    slice_band_group.remove(slice_band)

            return self

        except Exception as error:
            print(f'remove_band(), {error}')

    # Returns the x centres for all the slice bands
    def get_x_centres(self):
        return [slice_band.x_centre() for slice_band in self.slice_bands]

    # Returns the widths for all the slice bands
    def get_widths(self):
        return [slice_band.bounding_rectangle.width for slice_band in self.slice_bands]

    # Returns the mean width of the slice bands
    def get_mean_width(self):
        return np.mean(self.get_widths())

    # Removes bands which are less than or equal to 2 pixels in width from the slice bands.
    def remove_narrow_bands(self):
        minimum_width = 2

        narrow_bands = []

        for slice_band in self.slice_bands:
            if slice_band.bounding_rectangle.width <= minimum_width:
                narrow_bands.append(slice_band)

        for slice_band in narrow_bands:
            self.remove_band(slice_band)

        return self

    # Returns the heights for all the slice bands
    def get_heights(self):
        return [slice_band.bounding_rectangle.height for slice_band in self.slice_bands]

    # Returns the mean height for the slice bands
    def get_mean_height(self):
        return np.mean(self.get_heights())

    # Removes bands whose heights are less than the mean height / 4 (or 1 pixel).
    def remove_short_bands(self):
        try:
            height = self.get_mean_height()

            minimum_height = max(1, height / 4)

            short_bands = []

            for slice_band in self.slice_bands:
                if slice_band.bounding_rectangle.height <= minimum_height:
                    short_bands.append(slice_band)

            for slice_band in short_bands:
                self.remove_band(slice_band)

            return self

        except Exception as error:
            print(f'remove_short_bands(), {error}')

    # Returns the mean HSV variance
    def get_mean_hsv_variance(self):
        mean_hsv_variance = np.mean([slice_band.hsv_variance for slice_band in self.slice_bands])

        return mean_hsv_variance

    # Checks if input slice bands overlap with slice bands.
    def has_any_overlaps(self, slice_bands):
        for slice_band in slice_bands:

            if self is slice_band:
                continue

            if slice_band.has_overlap(slice_band):
                return True

        return False

    # Inserts slice band into slice band groups.
    @staticmethod
    def insert_into_slice_band_group(slice_band_groups, slice_band):

        for slice_band_group in slice_band_groups:

            if slice_band.has_any_overlaps(slice_band_group):
                slice_band_group.append(slice_band)
                return slice_band_groups

        slice_band_group = [slice_band]
        slice_band_groups.append(slice_band_group)

        return slice_band_groups
