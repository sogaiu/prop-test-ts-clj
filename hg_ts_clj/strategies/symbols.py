from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of

from .parameters import metadata_max

from hypothesis_grammar_clojure.symbols \
    import unqualified_symbol_as_str, \
           qualified_symbol_as_str

from ..verify.symbols import verify, \
    verify_with_metadata

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
            "verify": verify}

@composite
def qualified_symbol_items(draw):
    sym_str = draw(qualified_symbol_as_str())
    #
    return {"inputs": sym_str,
            "label": "symbol",
            "to_str": build_sym_str,
            "verify": verify}

@composite
def symbol_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    #
    sym_item = draw(one_of(unqualified_symbol_items(),
                           qualified_symbol_items()))
    #
    if not metadata:
        return sym_item
    else:
        # XXX: not sure about this approach
        sym_str = sym_item["to_str"](sym_item)
        #
        str_builder = make_form_with_metadata_str_builder(build_sym_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = \
            draw(lists(elements=metadata_items(label=metadata),
                       min_size=n, max_size=n))
        #
        return {"inputs": sym_str,
                "label": "symbol",
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items}
