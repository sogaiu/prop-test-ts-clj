from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max

from .atoms import atom_items
from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# vector: $ =>
#   seq(repeat($._metadata),
#       $._bare_vector),
#
# _bare_vector: $ =>
#   seq("[",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       "]"),

# XXX: could also have stuff before and after delimiters
def build_vector_str(vector_item):
    items = vector_item["inputs"]
    seps = vector_item["separators"]
    vector_elts = []
    for i, s in zip(items, seps):
        vector_elts += i["to_str"](i) + s
    return "[" + "".join(vector_elts) + "]"

@composite
def number_vector_items(draw):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": num_items,
            "label": "vector",
            "to_str": build_vector_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def atom_vector_items(draw):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": atm_items,
            "label": "vector",
            "to_str": build_vector_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}
