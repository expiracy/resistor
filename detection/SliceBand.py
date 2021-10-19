from detection.ResistorBand import ResistorBand


class SliceBand(ResistorBand):
    def __init__(self, colour, bounding_rectangle):
        super().__init__(colour)
        self.bounding_rectangle = bounding_rectangle
        self.dupe = False
