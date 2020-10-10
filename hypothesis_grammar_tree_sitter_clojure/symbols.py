from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of

from .parameters import metadata_max

from hypothesis_grammar_clojure.symbols \
    import unqualified_symbol_as_str, \
           qualified_symbol_as_str

from .verify import verify_node_as_atom

from .util import make_form_with_metadata_str_builder

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

def verify_symbol_node_with_metadata(ctx, item):
    # avoid circular dependency
    from .verify import verify_node_metadata
    #
    return verify_node_metadata(ctx, item) and \
        verify_node_as_atom(ctx, item)

@composite
def symbol_with_metadata_items(draw):
    # avoid circular dependency
    from .metadata import metadata_items
    #
    sym_item = draw(symbol_items())
    # XXX: not sure about this approach
    sym_str = sym_item["to_str"](sym_item)
    #
    str_builder = make_form_with_metadata_str_builder(build_sym_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=n, max_size=n))
    #
    return {"inputs": sym_str,
            "label": "symbol",
            "to_str": str_builder,
            "verify": verify_symbol_node_with_metadata,
            "metadata": md_items}
