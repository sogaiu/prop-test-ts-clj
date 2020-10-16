from hypothesis import assume
from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.characters \
    import any_character_as_str, \
           named_character_as_str, \
           octal_character_as_str, \
           unicode_quad_character_as_str

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_chr_str(item):
    return item["inputs"]

@composite
def any_character_items(draw):
    chr_str = draw(any_character_as_str())
    # XXX: tree-sitter cannot handle null byte (0)
    assume(chr_str != '\\\x00')
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def named_character_items(draw):
    chr_str = draw(named_character_as_str())
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def octal_character_items(draw):
    chr_str = draw(octal_character_as_str())
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def unicode_quad_character_items(draw):
    chr_str = draw(unicode_quad_character_as_str())
    #
    return {"inputs": chr_str,
            "label": label,
            "to_str": build_chr_str,
            "verify": verify}

@composite
def character_items(draw):
    chr_item = draw(one_of(any_character_items(),
                           named_character_items(),
                           octal_character_items(),
                           unicode_quad_character_items()))
    return chr_item
