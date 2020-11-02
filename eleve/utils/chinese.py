from typing import List

from ..preprocessing import chinese

from .. import Segmenter

def preproc_for_training(l: str) -> List[str]:
    chunks = chinese.tokenize_by_unicode_category(l)
    return [cjk for cjk in chinese.filter_cjk(chunks)]


def train(storage, data: List[str]):
    for line in data:
        cjks_chunks = preproc_for_training(line)
        for chunk in cjks_chunks:
            storage.add_sentence(list(chunk))
    return storage


def segment(storage, line: str) -> List[str]:
    seg = Segmenter(storage)
    tokens = []
    for group in chinese.tokenize_by_unicode_category(line):
        try:
            if chinese.isCJK(group[0]):
                words = ["".join(w) for w in seg.segment(list(group))]
                for w in words:
                    tokens.append(w)
            else:
                tokens.append(group)
        except:
            tokens.append(group)
    return tokens