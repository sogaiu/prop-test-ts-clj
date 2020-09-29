from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .atoms import atom_items
from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# list: $ =>
#   seq(repeat(choice(field('metadata', $.metadata),
#                     field('old_metadata', $.old_metadata),
#                     $._non_form)),
#       $._bare_list),
#
# _bare_list: $ =>
#   seq("(",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       ")"),

# XXX: could also have stuff before and after delimiters
def build_list_str(list_item):
    items = list_item["inputs"]
    seps = list_item["separators"]
    list_elts = []
    for i, s in zip(items, seps):
        list_elts += i["to_str"](i) + s
    return "(" + "".join(list_elts) + ")"

@composite
def number_list_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": num_items,
            "label": "list",
            "to_str": build_list_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def atom_list_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": atm_items,
            "label": "list",
            "to_str": build_list_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}
