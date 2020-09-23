from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.numbers \
    import radix_number_as_str, \
           hex_number_as_str, \
           octal_number_as_str, \
           ratio_as_str, \
           double_as_str, \
           integer_as_str

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "number", should the following be labeled
#      "hex_number"?
@composite
def hex_number_items(draw):
    a_num = draw(hex_number_as_str())
    #
    return (a_num, "number")

@composite
def octal_number_items(draw):
    a_num = draw(octal_number_as_str())
    #
    return (a_num, "number")

@composite
def radix_number_items(draw):
    a_num = draw(radix_number_as_str())
    #
    return (a_num, "number")

@composite
def ratio_items(draw):
    a_num = draw(ratio_as_str())
    #
    return (a_num, "number")

@composite
def double_items(draw):
    a_num = draw(double_as_str())
    #
    return (a_num, "number")

@composite
def integer_items(draw):
    a_num = draw(integer_as_str())
    #
    return (a_num, "number")

@composite
def number_items(draw):
    a_num, label = draw(one_of(radix_number_items(),
                               hex_number_items(),
                               octal_number_items(),
                               ratio_items(),
                               double_items(),
                               integer_items()))
    # XXX: whether label should be passed through...
    return (a_num, "number")
