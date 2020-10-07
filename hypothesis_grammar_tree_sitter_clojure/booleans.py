from hypothesis.strategies import composite, just, one_of

from .verify import verify_node_as_atom

# boolean: $ =>
#   choice('false',
#          'true'),

def build_boolean_str(item):
    return item["inputs"]

# XXX: may want to move parts to:
#
#        hypothesis_grammar_clojure.<something>
#
#     at some point
@composite
def boolean_items(draw):
    bool_str = draw(one_of(just("false"), just("true")))
    #
    return {"inputs": bool_str,
            "label": "boolean",
            "to_str": build_boolean_str,
            "verify": verify_node_as_atom}
