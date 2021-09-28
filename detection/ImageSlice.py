class ImageSlice:
    def __init__(self, image):
        self.image = image

    def slice(self):

        height = self.image.height()

        slice_height = round(height * 0.05)

        slice_amount = height // slice_height

        image_slices = []

        for slice_number in range(slice_amount):
            x = 0
            y = slice_number * slice_height

            image_slice = self.image.clone().region(x, y, self.image.width(), slice_height)

            image_slices.append(image_slice)

        return image_slices
