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

# set: $ =>
#   seq(repeat($._metadata),
#       $._bare_set),
#
# _bare_set: $ =>
#   seq("#{",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       "}"),

# XXX: could also have stuff before and after delimiters
def build_set_str(set_item):
    items = set_item["inputs"]
    seps = set_item["separators"]
    set_elts = []
    for i, s in zip(items, seps):
        set_elts += i["to_str"](i) + s
    return "#{" + "".join(set_elts) + "}"

@composite
def number_set_items(draw):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": num_items,
            "label": "set",
            "to_str": build_set_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def atom_set_items(draw):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": atm_items,
            "label": "set",
            "to_str": build_set_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}
