from enum import Enum, auto
import random as rnd

class CoopEnum(Enum):

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

    @classmethod
    def as_list(cls):
        return [e.name for e in cls]

    @classmethod
    def by_str(cls, str_name):

        # TODO: Not the best lookup strategy for large lists. Should better use the functions of Enum
        try:
            ret = cls[str_name]
        except:
            ret = next((item for item in cls if str(item) == str_name), None)

        return ret

    @classmethod
    def by_val(cls, val):
        return next(item for item in cls if item.value == val)

    @classmethod
    def random(cls):
        return rnd.choice(list(cls))


class CardinalPosition(CoopEnum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    TOP_CENTER = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    RIGHT_CENTER = auto()
    BOTTOM_CENTER = auto()
    LEFT_CENTER = auto()
    CENTER = auto()

if __name__=="__main__":
    class Dummy(CoopEnum):
        A = auto()
        B = auto()
        C = auto()

    print(Dummy.random())