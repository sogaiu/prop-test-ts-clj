from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.symbols \
    import unqualified_symbol_as_str, \
           qualified_symbol_as_str

from .verify import verify_node_as_atom

# const SYMBOL =
#       token(seq(SYMBOL_HEAD,
#                 repeat(SYMBOL_BODY)));

# _bare_symbol: $ =>
#   SYMBOL,

# symbol: $ =>
#   seq(repeat($._metadata),
#       $._bare_symbol),

def build_sym_str(item):
    return item["inputs"]

@composite
def unqualified_symbol_items(draw):
    sym_str = draw(unqualified_symbol_as_str())
    #
    return {"inputs": sym_str,
            "label": "symbol",
            "to_str": build_sym_str,
            "verify": verify_node_as_atom}

@composite
def qualified_symbol_items(draw):
    sym_str = draw(qualified_symbol_as_str())
    #
    return {"inputs": sym_str,
            "label": "symbol",
            "to_str": build_sym_str,
            "verify": verify_node_as_atom}

@composite
def symbol_items(draw):
    sym_item = draw(one_of(unqualified_symbol_items(),
                           qualified_symbol_items()))
    #
    return sym_item
