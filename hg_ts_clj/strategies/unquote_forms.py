from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import metadata_max

from .forms import form_items

from ..verify.unquote_forms import verify, \
    verify_with_metadata

from .util import make_form_with_metadata_str_builder

# unquote_form: $ =>
#   seq(repeat($._metadata),
#       field('marker', "~"),
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
def unquote_form_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    #
    form_item = draw(form_items())
    #
    if not metadata:
        return {"inputs": form_item,
                "label": "unquote_form",
                "to_str": build_unquote_form_str,
                "verify": verify,
                "marker": marker}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_unquote_form_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=n, max_size=n))
        #
        return {"inputs": form_item,
                "label": "unquote_form",
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items,
                "marker": marker}
