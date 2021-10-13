import cv2
import numpy
import os

from detection.ResistorLocator import ResistorLocator
from detection.BandFinder import BandFinder
from detection.Image import Image
from detection.Resistor import Resistor


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

        resistor_bands = BandFinder(self.image.clone()).find()

        self.resistor = Resistor(resistor_bands).main()

        return self.resistor, self.image






