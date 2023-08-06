from dataclasses import dataclass, field
from typing import Any, Callable

UNKNOWN_ATTR_DEFAULT = 0


@dataclass(frozen=True)
class Annotation:
    """
    An annotation is a matched entity in a text, with a text, a start- and end index (character),
    and a tag.
    """

    text: str
    start_char: int
    end_char: int
    tag: str
    length: int = field(init=False)

    def __post_init__(self):

        if len(self.text) != (self.end_char - self.start_char):
            raise ValueError("The span does not match the length of the text.")

        object.__setattr__(self, "length", self.end_char - self.start_char)

    def get_sort_key(
        self,
        by: list[str],
        callbacks: dict[str, Callable] = None,
        deterministic: bool = True,
    ) -> tuple[Any]:

        key = []

        for attr in by:

            val = getattr(self, attr, UNKNOWN_ATTR_DEFAULT)

            if callbacks is not None and (attr in callbacks):
                val = callbacks[attr](val)

            key.append(val)

        if deterministic:

            extra_attrs = sorted(set(self.__dict__.keys()) - set(by))

            for attr in extra_attrs:
                key.append(getattr(self, attr, UNKNOWN_ATTR_DEFAULT))

        return tuple(key)
