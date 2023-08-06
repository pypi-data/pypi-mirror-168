import re
from abc import ABC, abstractmethod
import itertools
from .token import Token


class BaseTokenizer(ABC):
    """A tokenizer tokenizes a piece of text."""

    @abstractmethod
    def tokenize(self, text: str, **kwargs) -> list[Token]:
        """
        Tokenize the text.

        Args:
            text: The input text.

        Returns: A list of Token, based on the input text.

        """


class SpaceSplitTokenizer(BaseTokenizer):
    """Tokenizer that splits text whenever a whitespace is present."""

    def tokenize(self, text: str, **kwargs) -> list[Token]:
        return [
            Token(text=match.group(0), start_char=match.start(), end_char=match.end(), index=counter)
            for counter, match in zip(itertools.count(), re.finditer(r"[^\s]+", text))
        ]
