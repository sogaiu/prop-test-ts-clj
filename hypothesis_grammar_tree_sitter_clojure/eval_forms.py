from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of

from .parameters import metadata_max

from .forms import form_items

from .lists import list_items
from .read_conds import read_cond_items
from .symbols import symbol_items

from .verify import verify_node_as_adorned, \
    verify_adorned_node_with_metadata

from .util import make_form_with_metadata_str_builder

# eval_form: $ =>
#   seq(repeat($._metadata), // ^:x #=(vector 1)
#       field('marker', "#="),
#       repeat($._non_form),
#       field('value', choice($.list,
#                             $.read_cond,
#                             // #= ^:a java.lang.String
#                             $.symbol))),

marker = '#='

# XXX: there is one separator of interest and that is potentially
#      between #= and the rest of the form.  the default here is
#      no separator.
def build_eval_form_str(item):
    inputs = item["inputs"]
    return marker + inputs["to_str"](inputs)

@composite
def eval_form_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    #
    legal_item = draw(one_of(list_items(elements=form_items()),
                             read_cond_items(),
                             symbol_items()))
    if not metadata:
        return {"inputs": legal_item,
                "label": "eval_form",
                "to_str": build_eval_form_str,
                "verify": verify_node_as_adorned,
                "marker": marker}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_eval_form_str)
        #
        n = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=n, max_size=n))
        #
        return {"inputs": legal_item,
                "label": "eval_form",
                "to_str": str_builder,
                "verify": verify_adorned_node_with_metadata,
                "metadata": md_items,
                "marker": marker}
