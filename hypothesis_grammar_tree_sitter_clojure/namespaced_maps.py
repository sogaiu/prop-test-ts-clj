from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

from .atoms import atom_items
from .keywords import keyword_items
from .numbers import number_items

from .verify import verify_node_as_atom, \
    verify_node_as_coll, \
    verify_node_with_prefix

# XXX: alternative ways of providing separation between elements?
#      obvious way is whitespace, but could also have:
#
#      * line comment that extends to end of line
#      * discard form
#      * combination
#
#      perhaps better to have a strategy for generating such
#      "spacing" or "separation" units
#
#      could also have stuff before and after delimiters
def build_namespaced_map_str(namespaced_map_item):
    items = namespaced_map_item["inputs"]
    prefix = namespaced_map_item["prefix"]
    return \
        "#" + \
        prefix["recipe"](prefix) + \
        "{" + \
        " ".join([item["recipe"](item) for item in items]) + \
        "}"

def build_auto_res_marker_str(item):
    # this is just "::"
    return item["inputs"]

@composite
def auto_res_marker_items(draw):
    arm_item = draw(just("::"))
    #
    return {"inputs": arm_item,
            "label": "auto_res_marker",
            "recipe": build_auto_res_marker_str,
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
    return {"inputs": num_items,
            "label": "namespaced_map",
            "recipe": build_namespaced_map_str,
            "verify": verify_node_with_prefix,
            "prefix": prefix_item}

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
    return {"inputs": atm_items,
            "label": "namespaced_map",
            "recipe": build_namespaced_map_str,
            "verify": verify_node_with_prefix,
            "prefix": prefix_item}
