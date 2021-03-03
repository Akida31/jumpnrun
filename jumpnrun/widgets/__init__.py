from enum import Enum


class XAlign(Enum):
    LEFT = 0,
    CENTER = 1,
    RIGHT = 2


class YAlign(Enum):
    TOP = 0,
    CENTER = 1,
    BOTTOM = 2


# reexport the content of the module
from .label import Label
from .button import Button
