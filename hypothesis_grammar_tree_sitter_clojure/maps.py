from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .atoms import atom_items
from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items

from .verify import verify_node_as_coll

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
def build_map_str(map_item):
    items = map_item["inputs"]
    return \
        "{" + \
        " ".join([item["recipe"](item) for item in items]) + \
        "}"

@composite
def number_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = n * 2
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=m, max_size=m))
    #
    return {"inputs": num_items,
            "label": "map",
            "recipe": build_map_str,
            "verify": verify_node_as_coll}

@composite
def atom_map_items(draw):
    n = draw(integers(min_value=0, max_value=10))
    m = 2 * n
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "map",
            "recipe": build_map_str,
            "verify": verify_node_as_coll}
