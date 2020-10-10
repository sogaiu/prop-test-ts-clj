from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import metadata_max

from .forms import form_items

from .verify import verify_node_as_adorned

from .util import make_form_with_metadata_str_builder

# deref_form: $ =>
#   seq(repeat($._metadata),
#       "@",
#       repeat($._non_form),
#       field('value', $._form)),

marker = '@'

# XXX: there is one separator of interest and that is potentially
#      between @ and the rest of the form.  the default here is
#      no separator.
def build_deref_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def deref_form_items(draw):
    form_item = draw(form_items())
    #
    return {"inputs": form_item,
            "label": "deref_form",
            "to_str": build_deref_form_str,
            "verify": verify_node_as_adorned,
            "marker": marker}

def verify_deref_form_node_with_metadata(ctx, item):
    # avoid circular dependency
    from .verify import verify_node_metadata
    #
    return verify_node_metadata(ctx, item) and \
        verify_node_as_adorned(ctx, item)

@composite
def deref_form_with_metadata_items(draw):
    # avoid circular dependency
    from .metadata import metadata_items
    #
    deref_form_item = draw(deref_form_items())
    #
    str_builder = make_form_with_metadata_str_builder(build_deref_form_str)
    #
    n = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=n, max_size=n))

    #
    return {"inputs": deref_form_item,
            "label": "deref_form",
            "to_str": str_builder,
            "verify": verify_deref_form_node_with_metadata,
            "metadata": md_items,
            "marker": marker}
