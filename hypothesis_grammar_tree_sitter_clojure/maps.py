from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, lists, one_of

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
def build_map_str(items):
    return "{" + " ".join([an_item for an_item, _ in items]) + "}"

@composite
def number_map_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    m = n * 2
    #
    num_items = draw(lists(elements=number_items(),
                           min_size=m, max_size=m))
    #
    map_item = (build_map_str(num_items), "map")
    #
    return (map_item, num_items)

@composite
def atom_items(draw):
    atm_item = draw(one_of(# XXX: boolean
                           character_items(),
                           keyword_items(),
                           # XXX: nil
                           number_items(),
                           # XXX: regex
                           string_items(),
                           symbol_items(),
                           # XXX: symbolic value
                          ))
    return atm_item

@composite
def atom_map_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    m = 2 * n
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=m, max_size=m))
    #
    map_item = (build_map_str(atm_items), "map")
    #
    return (map_item, atm_items)
