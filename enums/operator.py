from enum import Enum, auto



class Ops_(Enum):
    INCREMENT = auto()
    GROW = auto()
    MAX = auto()
    SET = auto()
    DECREMENT = auto()
    DIVIDE = auto()
    FLOOR_DIVIDE = auto()
    MULTIPLY = auto()
    PULL = auto()
    PUSH = auto()

    def compute(self, value1, value2):
        return opdict[self](value1, value2)


opdict = {
    Ops_.GROW: lambda x, y: max(x,y),
    Ops_.SET: lambda x, y: y,
    Ops_.DECREMENT: lambda x, y: x-y,
    Ops_.INCREMENT: lambda x, y: x+y,
    Ops_.FLOOR_DIVIDE: lambda x, y: x//y,
    Ops_.MULTIPLY: lambda x, y: x*y
}