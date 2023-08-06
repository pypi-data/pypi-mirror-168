from enum import IntEnum, EnumMeta


class _CustomMeta(EnumMeta):
    def __contains__(self, other):
        if isinstance(other, int):
            return other in [x.value for x in self]
        elif isinstance(other, str):
            return other in [x.name for x in self]


class Category(IntEnum, metaclass=_CustomMeta):
    General = 0
    Artist = 1
    Copyright = 3
    Character = 4
    Species = 5
    Invalid = 6
    Meta = 7
    Lore = 8
