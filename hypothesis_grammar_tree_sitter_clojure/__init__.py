import re

from hypothesis import assume
from hypothesis.strategies import booleans, characters, integers, text
from hypothesis.strategies import composite, just, lists, one_of, sampled_from

# XXX: clean these up later
# XXX: provide wrappers around these
from hypothesis_grammar_clojure.numbers import *
from hypothesis_grammar_clojure.symbols import *
from hypothesis_grammar_clojure.keywords import *

@composite
def integer_lists(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    int_strs = draw(lists(elements=integer_as_str(),
                          min_size=n, max_size=n))
    #
    return int_strs

@composite
def number_lists(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    num_strs = draw(lists(elements=number_as_str(),
                          min_size=n, max_size=n))
    #
    return num_strs

# XXX
@composite
def hetero_as_str(draw):
    het = draw(one_of(auto_resolved_keyword_as_str(),
                      # XXX: boolean
                      character_as_str(),
                      keyword_as_str(),
                      # XXX: nil
                      number_as_str(),
                      # XXX: regex
                      string_as_str(),
                      symbol_str(),
                      # XXX: symbolic value
                      ))
    return het

# XXX: should return not just values but their types too?
@composite
def hetero_lists(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    hets = draw(lists(elements=hetero_as_str(),
                      min_size=n, max_size=n))
    #
    return hets
