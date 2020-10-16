from hypothesis import assume
from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.characters \
    import any_character_as_str, \
           named_character_as_str, \
           octal_character_as_str, \
           unicode_quad_character_as_str

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

def build_chr_str(item):
    return item["inputs"]

@composite
def any_character_items(draw):
    a_chr_str = draw(any_character_as_str())
    # XXX: tree-sitter cannot handle null byte (0)
    assume(a_chr_str != '\\\x00')
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify}

@composite
def named_character_items(draw):
    a_chr_str = draw(named_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify}

@composite
def octal_character_items(draw):
    a_chr_str = draw(octal_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify}

@composite
def unicode_quad_character_items(draw):
    a_chr_str = draw(unicode_quad_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify}

@composite
def character_items(draw):
    a_chr_item = draw(one_of(any_character_items(),
                             named_character_items(),
                             octal_character_items(),
                             unicode_quad_character_items()))
    return a_chr_item
