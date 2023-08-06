import os
from enum import Enum
from functools import lru_cache
from typing import Type, List

from iobes import (
    parse_spans_iobes,
    parse_spans_iob,
    parse_spans_bilou,
    parse_spans_bmeow,
)
from pydantic import BaseModel
from pymultirole_plugins.v1.annotator import AnnotatorParameters, AnnotatorBase
from pymultirole_plugins.v1.schema import Document, Span, Annotation
from trankit import Pipeline

_home = os.path.expanduser("~")
xdg_cache_home = os.environ.get("XDG_CACHE_HOME") or os.path.join(_home, ".cache")


class Embeddings(str, Enum):
    xlm_roberta_base = "xlm-roberta-base"
    xlm_roberta_large = "xlm-roberta-large"


class TrankitNERParameters(AnnotatorParameters):
    # embeddings: Embeddings = Field(Embeddings.xlm_roberta_base,
    #                                description="""Which flavor of XLM-Roberta embeddings to use,
    # can be one of:<br/>
    # <li>`xlm-roberta-base`
    # <li>`xlm-roberta-large`
    # """)
    pass


SUPPORTED_LANGUAGES = {
    'ar': 'arabic',
    'zh': 'chinese',
    'nl': 'dutch',
    'en': 'english',
    'fr': 'french',
    'ru': 'russian',
    'es': 'spanish'
}


class TrankitNERAnnotator(AnnotatorBase):
    """[Trankit](https://trankit.readthedocs.io/en/latest/index.html) annotator.
    #need-segments
    #languages:""" + ','.join(SUPPORTED_LANGUAGES.keys())

    cache_dir = os.path.join(xdg_cache_home, "trankit")

    def annotate(
            self, documents: List[Document], parameters: AnnotatorParameters
    ) -> List[Document]:
        for document in documents:
            # Create cached pipeline context with language and embeddigns information
            lang = document_language(document, None)
            if lang is None or lang not in SUPPORTED_LANGUAGES:
                raise AttributeError(f"Metadata language {lang} is required and must be in {SUPPORTED_LANGUAGES}")
            p, tag_scheme = get_pipeline(
                SUPPORTED_LANGUAGES[lang], self.cache_dir, Embeddings.xlm_roberta_base.value
            )

            document.annotations = []
            if not document.sentences:
                document.sentences = [Span(start=0, end=len(document.text))]
            stexts = [document.text[s.start: s.end] for s in document.sentences]
            for sent, stext in zip(document.sentences, stexts):
                tagged_sent = p.ner(stext, is_sent=True)
                document.annotations.extend(
                    tags_to_anns(tag_scheme, tagged_sent, sent.start)
                )
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return TrankitNERParameters


def document_language(doc: Document, default: str = None):
    if doc.metadata is not None and 'language' in doc.metadata:
        return doc.metadata['language']
    return default


@lru_cache(maxsize=None)
def get_pipeline(lang, cache_dir, embeddings):
    p = Pipeline(lang, cache_dir=cache_dir, embedding=embeddings)
    tags = p._config.ner_vocabs[lang].keys()
    prefixes = sorted({t[0] for t in tags})
    tag_scheme = "".join(prefixes).lower()
    return p, tag_scheme


tags_parsers = {
    "beios": parse_spans_iobes,
    "bio": parse_spans_iob,
    "bilou": parse_spans_bilou,
    "bemow": parse_spans_bmeow,
}


def tags_to_anns(tag_scheme, tagged_sent, offset) -> List[Annotation]:
    anns: List[Annotation] = []
    text = tagged_sent["text"]
    tagged_tokens = tagged_sent["tokens"]
    tags = [t["ner"] for t in tagged_tokens]
    func = tags_parsers[tag_scheme]
    spans = func(tags)
    for span in spans:
        tok_start = tagged_tokens[span.start]["span"]
        tok_end = tagged_tokens[span.end - 1]["span"]
        ann = Annotation(
            start=tok_start[0] + offset,
            end=tok_end[1] + offset,
            text=text[tok_start[0]: tok_end[1]],
            label=span.type,
            labelName=span.type.lower(),
        )
        anns.append(ann)
    return anns
