from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

from .parameters import coll_max, metadata_max

from .forms import form_items
from .atoms import atom_items
from .keywords import keyword_items
from .numbers import number_items

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
#       "#",
#       field('prefix', choice($.auto_res_marker,
#                              $.keyword)),
#       repeat($._non_form),
#       $._bare_map),

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
    return "#" + prefix_str + "{" + "".join(ns_map_elts) + "}"

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
                "separators": sep_strs}
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
                "separators": sep_strs}

@composite
def number_namespaced_map_items(draw):
    number_ns_map_item = draw(namespaced_map_items(elements=number_items()))
    #
    return number_ns_map_item

@composite
def atom_namespaced_map_items(draw):
    atom_ns_map_item = draw(namespaced_map_items(elements=atom_items()))
    #
    return atom_ns_map_item
