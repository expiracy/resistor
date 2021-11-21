from enum import Enum


# Enum class for colours.
class Colour(Enum):
    UNKNOWN = -1,
    BLACK = 0,
    BROWN = 1,
    RED = 2,
    ORANGE = 3,
    YELLOW = 4,
    BLUE = 5,
    GREEN = 6,
    VIOLET = 7,
    GREY = 8,
    WHITE = 9,
    GOLD = 10,
    SILVER = 11

    def __str__(self):
        return self.name
