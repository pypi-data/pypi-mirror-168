import re
from abc import ABC, abstractmethod
from typing import Optional, Iterable

from docdeid.tokenize.tokenizer import BaseTokenizer
from docdeid.annotate.annotation import Annotation
from docdeid.ds import LookupList, LookupTrie
from docdeid.doc.document import Document
from docdeid.str.processor import BaseStringProcessor

class BaseAnnotator(ABC):
    """
    An annotator annotates a text based on its internal logic and rules, and outputs a list of annotations.
    """

    @abstractmethod
    def annotate(self, document: Document):
        """Annotate the document."""


class SingleTokenLookupAnnotator(BaseAnnotator):

    def __init__(self, lookup_values: Iterable, tag: str):

        self.lookup_list = LookupList()
        self.lookup_list.add_items_from_iterable(items=lookup_values)
        self.tag = tag
        super().__init__()

    def annotate(self, document: Document):
        tokens = document.tokens

        document.add_annotations(
            [
                Annotation(
                    text=token.text,
                    start_char=token.start_char,
                    end_char=token.end_char,
                    tag=self.tag,
                )
                for token in tokens
                if token.text in self.lookup_list
            ]
        )


class MultiTokenLookupAnnotator(BaseAnnotator):

    def __init__(self, lookup_values: Iterable, tokenizer: BaseTokenizer, tag: str, string_processors: Optional[list[BaseStringProcessor]] = None, **kwargs):

        self.trie = LookupTrie()
        self.tag = tag
        self.string_processors = string_processors

        for val in lookup_values:
            self.trie.add([token.text for token in tokenizer.tokenize(val, **kwargs)])

    @staticmethod
    def apply_string_processors(
        text: str, string_processors: list[BaseStringProcessor]
    ) -> str:
        """TODO: This should be a StringProcessingPipeline. Also now we have no guarantee there are no filters."""
        for string_processor in string_processors:
            text = string_processor.process_item(text)

        return text

    def annotate(self, document: Document):

        tokens = list(document.tokens)
        tokens_text = [token.text for token in tokens]

        if self.string_processors is not None:
            tokens_text = [
                self.apply_string_processors(text, self.string_processors)
                for text in tokens_text
            ]

        for i in range(len(tokens_text)):

            longest_matching_prefix = self.trie.longest_matching_prefix(
                tokens_text[i:]
            )

            if longest_matching_prefix is None:
                continue

            matched_tokens = tokens[i : i + len(longest_matching_prefix)]
            start_char = matched_tokens[0].start_char
            end_char = matched_tokens[-1].end_char

            document.add_annotation(
                Annotation(
                    text=document.text[start_char:end_char],
                    start_char=start_char,
                    end_char=end_char,
                    tag=self.tag,
                )
            )

            i += len(longest_matching_prefix)


class RegexpAnnotator(BaseAnnotator):
    """Annotate text based on regular expressions"""

    def __init__(
        self,
        regexp_pattern: re.Pattern,
        tag: str,
        capturing_group: int = 0,
    ):

        self.regexp_pattern = regexp_pattern
        self.tag = tag
        self.capturing_group = capturing_group
        super().__init__()

    def annotate(self, document: Document):

        for match in self.regexp_pattern.finditer(document.text):

            text = match.group(self.capturing_group)
            start, end = match.span(self.capturing_group)

            document.add_annotation(Annotation(text, start, end, self.tag))


class MetaDataAnnotator(BaseAnnotator):
    """A simple annotator that check the metadata (mainly testing)."""

    def __init__(self, tag: str):
        self.tag = tag
        super().__init__()

    def annotate(self, document: Document):

        for token in document.tokens:
            if token.text == document.get_meta_data_item("forbidden_string"):
                document.add_annotation(
                    Annotation(
                        token.text, token.start_char, token.end_char, self.tag
                    )
                )
