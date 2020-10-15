from hypothesis.strategies import composite

from ..verify.discard_exprs import verify

# discard_expr: $ =>
#   seq(field('marker', "#_"),
#       repeat($._non_form),
#       field('value', $._form)),

marker = '#_'

def build_discard_expr_str(item):
    form_item = item["inputs"]
    # XXX: space here should really be separator, but can
    #      also be empty string
    return marker + " " + form_item["to_str"](form_item)

# XXX: make another key-value pair for the repeat non_form?
@composite
def discard_expr_items(draw):
    # avoid circular dependency
    from .forms import form_items
    #
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "discard_expr",
            "to_str": build_discard_expr_str,
            "verify": verify,
            "marker": marker}