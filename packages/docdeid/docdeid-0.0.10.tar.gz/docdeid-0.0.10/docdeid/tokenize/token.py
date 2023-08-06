from dataclasses import dataclass


@dataclass(frozen=True)
class Token:

    text: str
    start_char: int
    end_char: int
    index: int
