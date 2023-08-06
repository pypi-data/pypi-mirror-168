from typing import Any, Callable, Iterable, Optional, Union

from docdeid.annotate.annotation import Annotation
from docdeid.annotate.annotation_processor import BaseAnnotationProcessor
from docdeid.annotate.redactor import BaseRedactor
from docdeid.tokenize.token import Token
from docdeid.tokenize.tokenizer import BaseTokenizer


class Document:
    """A document contains information on a single text, be it a phrase, sentence or paragraph."""

    def __init__(
        self,
        text: str,
        tokenizers: Optional[dict[str, BaseTokenizer]] = None,
        meta_data: Optional[dict] = None,
    ):

        self._text = text
        self._annotations = set()

        self._tokenizers = tokenizers
        self._meta_data = meta_data

        self._tokens = dict()
        self._deidentified_text = None

    @property
    def text(self) -> str:
        return self._text

    @property
    def tokens(self) -> list[Token]:

        return self.get_tokens()

    @property
    def annotations(self) -> set[Annotation]:

        return self._annotations.copy()

    def get_tokens(self, tokenizer_name: str = "default") -> list[Token]:

        if tokenizer_name not in self._tokenizers:
            raise ValueError(f"Cannot get tokens from unknown tokenizer {tokenizer_name}")

        if tokenizer_name not in self._tokens or self._tokens[tokenizer_name] is None:
            self._tokens[tokenizer_name] = self._tokenizers[tokenizer_name].tokenize(self._text)

        return self._tokens[tokenizer_name].copy()

    def get_annotations_sorted(
        self,
        by: list[str],
        callbacks: dict[str, Callable] = None,
        deterministic: bool = True,
    ) -> list[Annotation]:

        return sorted(
            list(self._annotations),
            key=lambda x: x.get_sort_key(
                by=by, callbacks=callbacks, deterministic=deterministic
            ),
        )

    @property
    def deidentified_text(self) -> str:

        return self._deidentified_text

    def get_meta_data(self) -> dict:
        return self._meta_data.copy()

    def get_meta_data_item(self, key: str) -> Union[Any, None]:

        if key not in self._meta_data:
            return None

        return self._meta_data[key]

    def add_meta_data_item(self, key: str, item: Any):

        if key in self._meta_data:
            raise ValueError(f"Key {key} already present in Document metadata, cannot overwrite (read only)")

        self._meta_data[key] = item

    def add_annotation(self, annotation: Annotation):

        self._annotations.add(annotation)

    def add_annotations(self, annotations: Iterable[Annotation]):

        for annotation in annotations:
            self._annotations.add(annotation)

    def apply_annotation_processor(self, processor: BaseAnnotationProcessor):

        if len(self._annotations) == 0:
            return

        self._annotations = processor.process(self._annotations, self.text)

    def apply_redactor(self, redactor: BaseRedactor):

        self._deidentified_text = redactor.redact(self.text, list(self._annotations))
