from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .atoms import atom_items
from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items

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
def build_vector_str(vector_item):
    items = vector_item["inputs"]
    return \
        "[" + \
        " ".join([item["recipe"](item) for item in items]) + \
        "]"

@composite
def number_vector_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=n, max_size=n))
    #
    return {"inputs": num_items,
            "label": "vector",
            "recipe": build_vector_str}

@composite
def atom_vector_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    #
    return {"inputs": atm_items,
            "label": "vector",
            "recipe": build_vector_str}
