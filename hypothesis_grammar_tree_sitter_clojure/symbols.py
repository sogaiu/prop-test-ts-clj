import re

from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.symbols \
    import unqualified_symbol_as_str, \
           qualified_symbol_as_str

from .verify import verify_node_as_atom

def build_sym_str(item):
    return item["inputs"]

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "symbol", should the following be labeled
#      "unqualified_symbol"?
@composite
def unqualified_symbol_items(draw):
    a_sym_str = draw(unqualified_symbol_as_str())
    #
    return {"inputs": a_sym_str,
            "label": "symbol",
            "recipe": build_sym_str,
            "verify": verify_node_as_atom}

@composite
def qualified_symbol_items(draw):
    a_sym_str = draw(qualified_symbol_as_str())
    #
    return {"inputs": a_sym_str,
            "label": "symbol",
            "recipe": build_sym_str,
            "verify": verify_node_as_atom}

@composite
def symbol_items(draw):
    a_sym_item = draw(one_of(unqualified_symbol_items(),
                             qualified_symbol_items()))
    #
    return a_sym_item
