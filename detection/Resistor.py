class Resistor:

    def __init__(self):
        self.bands = []
        self.type = 6

    @classmethod
    def create(cls):
        return Resistor()

    def identify_type(self, resistor):

        self.type = len(resistor)




