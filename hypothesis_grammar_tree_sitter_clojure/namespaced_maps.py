from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

from .parameters import coll_max, metadata_max

from .forms import form_items
from .keywords import keyword_items

from .separators import separator_strings

from .verify import verify_node_as_atom, \
    verify_node_as_coll, \
    verify_coll_node_with_metadata, \
    make_single_verifier

from .util import make_form_with_metadata_str_builder

# auto_res_marker: $ =>
#   AUTO_RESOLVE_MARKER,
#
# namespaced_map: $ =>
#   seq(repeat($._metadata),
#       field('marker', "#"),
#       field('prefix', choice($.auto_res_marker,
#                              $.keyword)),
#       repeat($._non_form),
#       $._bare_map),

marker = "#"
open_delim = "{"
close_delim = "}"

# XXX: could also have stuff before and after delimiters
def build_namespaced_map_str(namespaced_map_item):
    items = namespaced_map_item["inputs"]
    seps = namespaced_map_item["separators"]
    ns_map_elts = []
    for i, s in zip(items, seps):
        ns_map_elts += i["to_str"](i) + s
    #
    prefix = namespaced_map_item["prefix"]
    prefix_str = prefix["to_str"](prefix)
    #
    return marker + prefix_str + \
        open_delim + "".join(ns_map_elts) + close_delim

def build_auto_res_marker_str(item):
    # this is just "::"
    return item["inputs"]

@composite
def auto_res_marker_items(draw):
    arm_item = draw(just("::"))
    #
    return {"inputs": arm_item,
            "label": "auto_res_marker",
            "to_str": build_auto_res_marker_str,
            "verify": verify_node_as_atom}

@composite
def prefix_items(draw):
    prefix_item = draw(one_of(auto_res_marker_items(),
                              keyword_items()))
    return prefix_item

def verify(ctx, item):
    return make_single_verifier("prefix")(ctx, item) and \
        verify_node_as_coll(ctx, item)

def verify_with_metadata(ctx, item):
    return make_single_verifier("prefix")(ctx, item) and \
        verify_coll_node_with_metadata(ctx, item)

@composite
def namespaced_map_items(draw, elements=form_items(), metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    # XXX: what about this /2?
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    prefix_item = draw(prefix_items())
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    if not metadata:
        return {"inputs": items,
                "label": "namespaced_map",
                "to_str": build_namespaced_map_str,
                "verify": verify,
                "prefix": prefix_item,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
    else:
        str_builder = \
            make_form_with_metadata_str_builder(build_namespaced_map_str)
        #
        m = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=m, max_size=m))
        #
        return {"inputs": items,
                "label": "namespaced_map",
                "to_str": str_builder,
                "verify": verify_with_metadata,
                "prefix": prefix_item,
                "metadata": md_items,
                "separators": sep_strs,
                "marker": marker,
                "open": open_delim,
                "close": close_delim}
