from hypothesis.strategies import composite

from .forms import form_items

from .verify import verify_node_as_adorned

# var_quote_form: $ =>
#   seq(repeat($._metadata),
#       "#'",
#       repeat($._non_form),
#       // XXX: symbol, reader conditional, and tagged literal can work
#       //      any other things?
#       field('value', $._form)),

# XXX: there is one separator of interest and that is potentially
#      between #' and the rest of the form.  the default here is
#      no separator.
def build_var_quote_form_str(item):
    inputs = item["inputs"]
    return "#'" + inputs["to_str"](inputs)

@composite
def var_quote_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "var_quote_form",
            "to_str": build_var_quote_form_str,
            "verify": verify_node_as_adorned}