from hypothesis.strategies import composite, one_of

from .characters import character_items
from .keywords import keyword_items
from .numbers import number_items
from .strings import string_items
from .symbols import symbol_items

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
