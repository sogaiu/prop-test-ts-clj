from hypothesis import assume
from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.characters \
    import any_character_as_str, \
           named_character_as_str, \
           octal_character_as_str, \
           unicode_quad_character_as_str

from .verify import verify_node_as_atom

# const CHARACTER =
#       token(seq("\\",
#                 choice(OCTAL_CHAR,
#                        NAMED_CHAR,
#                        UNICODE,
#                        ANY_CHAR)));

def build_chr_str(item):
    return item["inputs"]

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "character", should the following be labeled
#      "any_character"?
@composite
def any_character_items(draw):
    a_chr_str = draw(any_character_as_str())
    # XXX: tree-sitter cannot handle null byte (0)
    assume(a_chr_str != '\\\x00')
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify_node_as_atom}

@composite
def named_character_items(draw):
    a_chr_str = draw(named_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify_node_as_atom}

@composite
def octal_character_items(draw):
    a_chr_str = draw(octal_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify_node_as_atom}

@composite
def unicode_quad_character_items(draw):
    a_chr_str = draw(unicode_quad_character_as_str())
    #
    return {"inputs": a_chr_str,
            "label": "character",
            "to_str": build_chr_str,
            "verify": verify_node_as_atom}

@composite
def character_items(draw):
    a_chr_item = draw(one_of(any_character_items(),
                             named_character_items(),
                             octal_character_items(),
                             unicode_quad_character_items()))
    return a_chr_item
