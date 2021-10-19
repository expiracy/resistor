import cv2
import numpy
import os

from detection.ResistorLocator import ResistorLocator
from detection.SliceBandFinder import SliceBandFinder
from detection.Image import Image
from detection.Resistor import Resistor
from detection.BandIdentifier import BandIdentifier
from detection.SliceBandSelector import SliceBandSelector


class Detector:

    def __init__(self):
        self.image = None
        self.resistor = None

    def detect(self, location):
        self.image = Image().load(location)

        if self.image.width() > 1280:
            ratio = self.image.width() / self.image.height()

            scale = 1280 / ratio

            self.image.resize(1280, round(scale))

        self.image = ResistorLocator(self.image).locate()

        self.image.show()

        slice_bands = SliceBandFinder(self.image.clone()).find()

        possible_bands = SliceBandSelector(slice_bands).find_possible_bands()

        resistor_bands = BandIdentifier(possible_bands, slice_bands).find_resistor_bands()

        self.resistor = Resistor(resistor_bands).main()

        return self.resistor, self.image






