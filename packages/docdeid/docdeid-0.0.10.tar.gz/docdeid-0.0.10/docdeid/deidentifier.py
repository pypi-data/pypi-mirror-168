from typing import Optional, Union

from docdeid.annotate.annotation_processor import BaseAnnotationProcessor
from docdeid.annotate.annotator import BaseAnnotator
from docdeid.annotate.redactor import BaseRedactor
from docdeid.doc.document import Document
from docdeid.tokenize.tokenizer import BaseTokenizer

from collections import OrderedDict


class DocDeid:

    def __init__(
        self,
    ):

        self._tokenizers = {}
        self._annotators = OrderedDict()
        self._annotation_postprocessors = OrderedDict()
        self._redactor = None

    def add_annotator(self, name: str, annotator: BaseAnnotator):
        self._annotators[name] = annotator

    def remove_annotator(self, name: str):
        del self._annotators[name]

    def add_annotation_postprocessor(
        self, name: str, annotation_postprocessor: BaseAnnotationProcessor
    ):
        self._annotation_postprocessors[name] = annotation_postprocessor

    def remove_annotation_postprocessor(self, name: str):
        del self._annotation_postprocessors[name]

    def set_redactor(self, redactor: BaseRedactor):
        self._redactor = redactor

    def add_tokenizer(self, name: str, tokenizer: BaseTokenizer):
        self._tokenizers[name] = tokenizer

    def remove_tokenizer(self, name: str):
        del self._tokenizers[name]

    def _annotate(
        self, document: Document, annotators_enabled: list[str] = None
    ):

        if annotators_enabled is None:
            annotators_enabled = self._annotators.keys()

        for annotator_name in annotators_enabled:
            self._annotators[annotator_name].annotate(document)

    def _postprocess_annotations(self, document: Document):

        for annotation_processor in self._annotation_postprocessors.values():
            document.apply_annotation_processor(annotation_processor)

    def _redact(self, annotated_document: Document):

        if self._redactor is not None:
            annotated_document.apply_redactor(self._redactor)

    def deidentify(
        self,
        text: str,
        annotators_enabled: list[str] = None,
        meta_data: Optional[dict] = None,
        return_as_text: Optional[bool] = False,
    ) -> Union[Document, str]:

        document = Document(text, tokenizers=self._tokenizers, meta_data=meta_data)

        self._annotate(document, annotators_enabled)
        self._postprocess_annotations(document)
        self._redact(document)

        if return_as_text:
            return document.deidentified_text

        return document
