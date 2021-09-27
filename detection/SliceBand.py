from detection.ResistorBand import ResistorBand


class SliceBand(ResistorBand):
    def __init__(self, colour, bounding_rectangle):
        super().__init__(colour, bounding_rectangle)
