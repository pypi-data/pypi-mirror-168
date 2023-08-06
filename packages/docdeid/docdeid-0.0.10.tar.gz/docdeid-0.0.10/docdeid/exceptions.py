from enum import Enum, auto


class ErrorHandling(Enum):
    RAISE = auto()
    REDACT = auto()
    WARN_AND_CONTINUE = auto()
