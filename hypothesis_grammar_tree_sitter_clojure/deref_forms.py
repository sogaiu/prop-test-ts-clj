from hypothesis.strategies import composite

from .forms import form_items

from .verify import verify_node_as_adorned

# deref_form: $ =>
#   seq(repeat(choice(field('metadata', $.metadata),
#                     field('old_metadata', $.old_metadata),
#                     $._non_form)),
#       "@",
#       repeat($._non_form),
#       field('value', $._form)),

# XXX: there is one separator of interest and that is potentially
#      between @ and the rest of the form.  the default here is
#      no separator.
def build_deref_form_str(item):
    inputs = item["inputs"]
    return "@" + inputs["to_str"](inputs)

@composite
def deref_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "deref_form",
            "to_str": build_deref_form_str,
            "verify": verify_node_as_adorned}
