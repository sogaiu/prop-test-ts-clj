from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import metadata_max

from .forms import form_items

from .verify import verify_node_as_adorned, \
    verify_adorned_node_with_metadata

from .util import make_form_with_metadata_str_builder

# var_quote_form: $ =>
#   seq(repeat($._metadata),
#       "#'",
#       repeat($._non_form),
#       // XXX: symbol, reader conditional, and tagged literal can work
#       //      any other things?
#       field('value', $._form)),

marker = "#'"

# XXX: there is one separator of interest and that is potentially
#      between #' and the rest of the form.  the default here is
#      no separator.
def build_var_quote_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def var_quote_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "var_quote_form",
            "to_str": build_var_quote_form_str,
            "verify": verify_node_as_adorned,
            "marker": marker}

@composite
def var_quote_form_with_metadata_items(draw):
    # avoid circular dependency
    from .metadata import metadata_items
    #
    var_quote_form_item = draw(var_quote_form_items())
    #
    str_builder = \
        make_form_with_metadata_str_builder(build_var_quote_form_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=n, max_size=n))
    #
    return {"inputs": var_quote_form_item,
            "label": "var_quote_form",
            "to_str": str_builder,
            "verify": verify_adorned_node_with_metadata,
            "metadata": md_items,
            "marker": marker}
