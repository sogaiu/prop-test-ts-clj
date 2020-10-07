from hypothesis.strategies import composite, just, one_of

from .symbols import symbol_items

from .verify import verify_node_as_adorned

# symbolic_value: $ =>
#   seq("##",
#       repeat($._non_form),
#       field('value', $.symbol)),

marker = '##'

def build_symbolic_value_str(item):
    sym_item = item["inputs"]
    # XXX: there can be one or more non_forms between the marker and symbol...
    return marker + sym_item["to_str"](sym_item)

# XXX: may want to move parts to:
#
#        hypothesis_grammar_clojure.<something>
#
#     at some point
@composite
def symbolic_value_items(draw):
    sym_val_str = draw(one_of(just("Inf"), just("-Inf"), just("NaN")))
    #
    # XXX: a bit of a hack?
    sym_item = draw(symbol_items())
    sym_item["inputs"] = sym_val_str
    #
    return {"inputs": sym_item,
            "label": "symbolic_value",
            "to_str": build_symbolic_value_str,
            "verify": verify_node_as_adorned,
            "marker": marker}
