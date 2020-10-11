from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import metadata_max

from .forms import form_items

from .verify import verify_node_as_adorned, \
    verify_adorned_node_with_metadata

from .util import make_form_with_metadata_str_builder

# quote_form: $ =>
#   seq(repeat($._metadata),
#       "'",
#       repeat($._non_form),
#       field('value', $._form)),

marker = "'"

# XXX: there is one separator of interest and that is potentially
#      between ' and the rest of the form.  the default here is
#      no separator.
def build_quote_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def quote_form_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    #
    form_item = draw(form_items())
    #
    if not metadata:
        return {"inputs": form_item,
                "label": "quote_form",
                "to_str": build_quote_form_str,
                "verify": verify_node_as_adorned,
                "marker": marker}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_quote_form_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=n, max_size=n))
        #
        return {"inputs": form_item,
                "label": "quote_form",
                "to_str": str_builder,
                "verify": verify_adorned_node_with_metadata,
                "metadata": md_items,
                "marker": marker}
