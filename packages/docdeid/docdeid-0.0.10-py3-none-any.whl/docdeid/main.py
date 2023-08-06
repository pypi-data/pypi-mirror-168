import docdeid
from docdeid.ds.lookup import LookupList
from docdeid.doc.document import Document
from docdeid.tokenize.tokenizer import SpaceSplitTokenizer

from docdeid.annotate.annotation_processor import OverlapResolver

from dataclasses import dataclass

def main():

    lr = OverlapResolver(sort_by=['start_char'])  # left to right
    ls = OverlapResolver(sort_by=['is_patient', 'length'], sort_by_callbacks={'is_patient': lambda x: -x, 'length': lambda x: -x})  # long to short

    @dataclass(frozen=True)
    class CustomAnnotation(docdeid.Annotation):
        is_patient: bool

    annotations = {
        CustomAnnotation(text="_" * 2, start_char=10, end_char=12, tag="left", is_patient=True),
        CustomAnnotation(text="_" * 10, start_char=5, end_char=15, tag="right", is_patient=False)
    }

    ann = ls.process(annotations, text="_" * 15)
    print(ann)

    print("done")


if __name__ == "__main__":
    main()
