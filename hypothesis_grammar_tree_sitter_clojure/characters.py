from hypothesis import assume
from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.characters \
    import any_character_as_str, \
           named_character_as_str, \
           octal_character_as_str, \
           unicode_quad_character_as_str

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "character", should the following be labeled
#      "any_character"?
@composite
def any_character_items(draw):
    a_chr = draw(any_character_as_str())
    # XXX: tree-sitter cannot handle null byte (0)
    assume(a_chr != '\\\x00')
    #
    return (a_chr, "character")

@composite
def named_character_items(draw):
    a_chr = draw(named_character_as_str())
    #
    return (a_chr, "character")

@composite
def octal_character_items(draw):
    a_chr = draw(octal_character_as_str())
    #
    return (a_chr, "character")

@composite
def unicode_quad_character_items(draw):
    a_chr = draw(unicode_quad_character_as_str())
    #
    return (a_chr, "character")

@composite
def character_items(draw):
    a_chr, label = draw(one_of(any_character_items(),
                               named_character_items(),
                               octal_character_items(),
                               unicode_quad_character_items()))
    # XXX: whether label should be passed through...
    return (a_chr, "character")
