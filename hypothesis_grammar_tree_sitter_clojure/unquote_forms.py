from hypothesis.strategies import composite

from .forms import form_items

from .verify import verify_node_as_adorned

# unquote_form: $ =>
#   seq(repeat($._metadata),
#       "~",
#       repeat($._non_form),
#       field('value', $._form)),

marker = "~"

# XXX: there is one separator of interest and that is potentially
#      between ` and the rest of the form.  the default here is
#      no separator.
def build_unquote_form_str(item):
    inputs = item["inputs"]
    form_str = inputs["to_str"](inputs)
    # to avoid misinterpretation, the following is done
    sep = ""
    if form_str[0] == "@":
        sep = " "
    return marker + sep + form_str

@composite
def unquote_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "unquote_form",
            "to_str": build_unquote_form_str,
            "verify": verify_node_as_adorned,
            "marker": marker}
