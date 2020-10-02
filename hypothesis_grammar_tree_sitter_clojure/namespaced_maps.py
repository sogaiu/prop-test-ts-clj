from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

from .atoms import atom_items
from .keywords import keyword_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_atom, \
    verify_node_as_coll, \
    verify_node_with_prefix

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
            # looks like this happens to work
            "verify": verify_node_as_atom}

@composite
def prefix_items(draw):
    prefix_item = draw(one_of(auto_res_marker_items(),
                              keyword_items()))
    #
    return prefix_item

@composite
def number_namespaced_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = n * 2
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=m, max_size=m))
    #
    prefix_item = draw(prefix_items())
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=m, max_size=m))
    #
    return {"inputs": num_items,
            "label": "namespaced_map",
            "to_str": build_namespaced_map_str,
            "verify": verify_node_with_prefix,
            "prefix": prefix_item,
            "separators": sep_strs}

@composite
def atom_namespaced_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = 2 * n
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=m, max_size=m))
    #
    prefix_item = draw(prefix_items())
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "namespaced_map",
            "to_str": build_namespaced_map_str,
            "verify": verify_node_with_prefix,
            "prefix": prefix_item,
            "separators": sep_strs}
