import re
from abc import ABC, abstractmethod
from typing import Optional, Callable

import numpy as np

from docdeid.annotate.annotation import Annotation


class BaseAnnotationProcessor(ABC):

    @abstractmethod
    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:
        pass


class OverlapResolver(BaseAnnotationProcessor):

    def __init__(self, sort_by: list[str], sort_by_callbacks: Optional[dict[str, Callable]] = None, deterministic: bool = True):
        self._sort_by = sort_by
        self._sort_by_callbacks = sort_by_callbacks
        self._deterministic = deterministic

    @staticmethod
    def _zero_runs(a: np.array) -> list[tuple[int, int]]:
        """
        Finds al zero runs in an numpy array.
        From: https://stackoverflow.com/questions/24885092/finding-the-consecutive-zeros-in-a-numpy-array
        """

        iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
        absdiff = np.abs(np.diff(iszero))
        return np.where(absdiff == 1)[0].reshape(-1, 2)

    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:

        if len(annotations) == 0:
            return annotations

        mask = np.zeros(max(annotation.end_char for annotation in annotations))
        processed_annotations = set()

        sorted_annotations = sorted(
            list(annotations),
            key=lambda a: a.get_sort_key(by=self._sort_by, callbacks=self._sort_by_callbacks, deterministic=self._deterministic),
        )

        for annotation in sorted_annotations:

            mask_annotation = mask[annotation.start_char : annotation.end_char]

            if sum(mask_annotation) == 0:  # no overlap
                processed_annotations.add(annotation)

            else:  # overlap

                for start_char_run, end_char_run in self._zero_runs(mask_annotation):

                    processed_annotations.add(
                        Annotation(
                            text=annotation.text[start_char_run:end_char_run],
                            start_char=annotation.start_char + start_char_run,
                            end_char=annotation.start_char + end_char_run,
                            tag=annotation.tag,
                        )
                    )

            mask[annotation.start_char : annotation.end_char] = 1

        return processed_annotations


class MergeAdjacentAnnotations(BaseAnnotationProcessor):

    def __init__(self, slack_regexp: str = None, check_overlap: bool = True):
        self.slack_regexp = slack_regexp
        self.check_overlap = check_overlap

    @staticmethod
    def has_overlapping_annotations(annotations: set[Annotation]) -> bool:
        """TODO: Make this a property of Annotation or AnnotationSet?"""

        annotations = sorted(
            list(annotations), key=lambda a: a.get_sort_key(by=["start_char"])
        )

        for annotation, next_annotation in zip(annotations, annotations[1:]):
            if annotation.end_char > next_annotation.start_char:
                return True

        return False

    def _tags_match(self, left_tag: str, right_tag: str) -> bool:

        return left_tag == right_tag

    def _tag_replacement(self, left_tag: str, right_tag: str) -> str:

        return left_tag

    def _are_adjacent_annotations(
        self, left_annotation: Annotation, right_annotation: Annotation, text: str
    ) -> bool:

        if not self._tags_match(
            left_annotation.tag, right_annotation.tag
        ):
            return False

        between_text = text[left_annotation.end_char : right_annotation.start_char]

        if self.slack_regexp is None:
            return between_text == ""
        else:
            return re.fullmatch(self.slack_regexp, between_text) is not None

    def _adjacent_annotations_replacement(
        self, left_annotation: Annotation, right_annotation: Annotation, text: str
    ) -> Annotation:

        return Annotation(
            text=f"{left_annotation.text}"
            f"{text[left_annotation.end_char: right_annotation.start_char]}"
            f"{right_annotation.text}",
            start_char=left_annotation.start_char,
            end_char=right_annotation.end_char,
            tag=self._tag_replacement(
                left_annotation.tag, right_annotation.tag
            ),
        )

    def process(self, annotations: set[Annotation], text: str) -> set[Annotation]:

        if self.check_overlap and self.has_overlapping_annotations(annotations):
            raise ValueError(
                f"{self.__class__} received input with overlapping annotations."
            )

        processed_annotations = set()

        annotations = sorted(
            list(annotations),
            key=lambda a: a.get_sort_key(by=["start_char"]),
        )

        for index in range(len(annotations) - 1):

            annotation, next_annotation = annotations[index], annotations[index + 1]

            if self._are_adjacent_annotations(annotation, next_annotation, text):
                annotations[index + 1] = self._adjacent_annotations_replacement(
                    annotation, next_annotation, text
                )
            else:
                processed_annotations.add(annotation)

        processed_annotations.add(annotations[-1])  # add last one

        return processed_annotations
