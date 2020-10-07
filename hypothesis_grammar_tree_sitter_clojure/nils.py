from hypothesis.strategies import composite, just, one_of

from .verify import verify_node_as_atom

# nil: $ =>
#   'nil',

def build_nil_str(item):
    return item["inputs"]

# XXX: may want to move parts to:
#
#        hypothesis_grammar_clojure.<something>
#
#     at some point
@composite
def nil_items(draw):
    nil_str = draw(just("nil"))
    #
    return {"inputs": nil_str,
            "label": "nil",
            "to_str": build_nil_str,
            "verify": verify_node_as_atom}
