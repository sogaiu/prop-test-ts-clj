from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# XXX: could also have stuff before and after delimiters
def build_map_str(map_item):
    items = map_item["inputs"]
    seps = map_item["separators"]
    map_elts = []
    for i, s in zip(items, seps):
        map_elts += i["recipe"](i) + s
    return "{" + "".join(map_elts) + "}"

@composite
def number_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = n * 2
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=m, max_size=m))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=m, max_size=m))
    #
    return {"inputs": num_items,
            "label": "map",
            "recipe": build_map_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def atom_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = 2 * n
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=m, max_size=m))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "map",
            "recipe": build_map_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}
