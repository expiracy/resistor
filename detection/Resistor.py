class Resistor:

    def __init__(self):
        self.bands = []
        self.type = 6

    @classmethod
    def create(cls):
        return Resistor()


