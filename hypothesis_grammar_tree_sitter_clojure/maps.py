from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# map: $ =>
#   seq(repeat($._metadata),
#       $._bare_map),
#
# _bare_map: $ =>
#   seq("{",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       "}"),

# XXX: could also have stuff before and after delimiters
def build_map_str(map_item):
    items = map_item["inputs"]
    seps = map_item["separators"]
    map_elts = []
    for i, s in zip(items, seps):
        map_elts += i["to_str"](i) + s
    return "{" + "".join(map_elts) + "}"

@composite
def map_items(draw, elements):
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": items,
            "label": "map",
            "to_str": build_map_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def number_map_items(draw):
    number_map_item = draw(map_items(elements=number_items()))
    #
    return number_map_item

@composite
def atom_map_items(draw):
    atom_map_item = draw(map_items(elements=atom_items()))
    #
    return atom_map_item
