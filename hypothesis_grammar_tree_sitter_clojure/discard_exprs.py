from hypothesis.strategies import composite

from .verify import verify_node_as_discard_expr

# discard_expr: $ =>
#   seq("#_",
#       repeat($._non_form),
#       field('value', $._form)),

# XXX: could use a lookup table for all markers that's keyed by label?
marker = '#_'

def build_discard_expr_str(item):
    form_item = item["inputs"]
    # XXX: space here should really be separator, but can
    #      also be empty string
    return marker + " " + form_item["to_str"](form_item)

# XXX: make another key-value pair for the repeat non_form?
@composite
def discard_expr_items(draw):
    # coping with circular imports
    from .forms import form_items
    #
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "discard_expr",
            "to_str": build_discard_expr_str,
            "verify": verify_node_as_discard_expr,
            "marker": marker}
