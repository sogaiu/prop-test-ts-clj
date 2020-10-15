from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .forms import form_items

from .separators import separator_strings

from ..verify.anon_funcs import verify, \
    verify_with_metadata

from .util import make_form_with_metadata_str_builder

# anon_func: $ =>
#   seq(repeat($._metadata),
#       field('marker', "#"),
#       $._bare_list),
#
# _bare_list: $ =>
#   seq(field('open', "("),
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       field('close', ")")),

marker = "#"
open_delim = "("
close_delim = ")"

# XXX: could also have stuff after delimiters
def build_anon_func_str(anon_func_item):
    items = anon_func_item["inputs"]
    seps = anon_func_item["separators"]
    anon_func_elts = []
    for i, s in zip(items, seps):
        anon_func_elts += i["to_str"](i) + s
    return marker + open_delim + "".join(anon_func_elts) + close_delim

# def verify(ctx, item):
#     return verify_node_as_coll(ctx, item) and \
#         verify_node_marker(ctx, item)

# def verify_with_metadata(ctx, item):
#     return verify_coll_node_with_metadata(ctx, item) and \
#         verify_node_marker(ctx, item)

@composite
def anon_func_items(draw, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    #
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements=form_items(),
                       min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    if not metadata:
        return {"inputs": items,
                "label": "anon_func",
                "to_str": build_anon_func_str,
                "verify": verify,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
    else:
        str_builder = make_form_with_metadata_str_builder(build_anon_func_str)
        #
        m = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=m, max_size=m))
        #
        return {"inputs": items,
                "label": "anon_func",
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "metadata": md_items,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
