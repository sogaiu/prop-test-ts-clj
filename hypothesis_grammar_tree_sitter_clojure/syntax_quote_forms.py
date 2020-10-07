from hypothesis.strategies import composite

from .forms import form_items

from .verify import verify_node_as_adorned

# syntax_quote_form: $ =>
#   seq(repeat($._metadata),
#       "`",
#       repeat($._non_form),
#       field('value', $._form)),

marker = "`"

# XXX: there is one separator of interest and that is potentially
#      between ` and the rest of the form.  the default here is
#      no separator.
def build_syntax_quote_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def syntax_quote_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "syntax_quote_form",
            "to_str": build_syntax_quote_form_str,
            "verify": verify_node_as_adorned,
            "marker": marker}