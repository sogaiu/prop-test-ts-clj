import re

from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.symbols \
    import unqualified_symbol_as_str, \
           qualified_symbol_as_str

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "symbol", should the following be labeled
#      "unqualified_symbol"?
@composite
def unqualified_symbol_items(draw):
    a_sym = draw(unqualified_symbol_as_str())
    #
    return (a_sym, "symbol")

@composite
def qualified_symbol_items(draw):
    a_sym = draw(qualified_symbol_as_str())
    #
    return (a_sym, "symbol")

@composite
def symbol_items(draw):
    a_sym, label = draw(one_of(unqualified_symbol_items(),
                               qualified_symbol_items()))
    # XXX: whether label should be passed through...
    return (a_sym, "symbol")
