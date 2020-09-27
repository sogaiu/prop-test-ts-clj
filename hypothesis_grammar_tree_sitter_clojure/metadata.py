from hypothesis.strategies import integers, lists
from hypothesis.strategies import composite, one_of

# XXX: clean up later
# XXX: add reader conditionals at some point?
from .keywords import *
# XXX: want generic (i.e. not just atoms) map_items eventually?
from .maps import atom_map_items
from .strings import string_items
from .symbols import symbol_items
# metadatee-related (maps and symbols from above would be too)
from .atoms import atom_items
from .vectors import atom_vector_items, build_vector_str
# XXX: clean up later
from .verify import verify_node_as_atom, \
    verify_node_as_coll, \
    verify_node_with_metadata

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
#      there is one separator of interest and that is potentially
#      between ^ and the rest of the form.  the default here is
#      no separator.
def build_metadata_str(md_item):
    inner_item = md_item["inputs"]
    return f'^{inner_item["recipe"](inner_item)}'

# XXX: factor out?
def attach_metadata(metadata_str, metadatee_str):
    # XXX: another "what to do about separator" location
    return metadata_str + " " + metadatee_str

# XXX: only handles single piece of metadata atm
def build_vector_with_metadata_str(item):
    vec_str = build_vector_str(item)
    #
    md_items = item["metadata"]
    # XXX: only handles single piece of metadata atm
    md_str = build_metadata_str(md_items[0])
    #
    return attach_metadata(md_str, vec_str)

# XXX: only non-auto-resolved-keywords are valid
@composite
def keyword_metadata_items(draw):
    keyword_item = draw(one_of(unqualified_keyword_items(),
                               qualified_keyword_items()))
    #
    return {"inputs": keyword_item,
            "label": "metadata",
            "recipe": build_metadata_str,
            "verify": verify_node_as_atom}

# (source [0, 0] - [1, 0]
#   (vector [0, 0] - [0, 12]
#     metadata: (metadata [0, 0] - [0, 7]
#       (map [0, 1] - [0, 7]
#         value: (keyword [0, 2] - [0, 4])
#         value: (number [0, 5] - [0, 6])))
#     value: (keyword [0, 9] - [0, 11])))
@composite
def map_metadata_items(draw):
    map_item = draw(atom_map_items())
    #
    return {"inputs": map_item,
            "label": "metadata",
            "recipe": build_metadata_str,
            "verify": verify_node_as_coll}

@composite
def string_metadata_items(draw):
    string_item = draw(string_items())
    #
    return {"inputs": string_item,
            "label": "metadata",
            "recipe": build_metadata_str,
            "verify": verify_node_as_atom}

@composite
def symbol_metadata_items(draw):
    symbol_item = draw(symbol_items())
    #
    return {"inputs": symbol_item,
            "label": "metadata",
            "recipe": build_metadata_str,
            "verify": verify_node_as_atom}

@composite
def metadata_items(draw):
    metadata_item = draw(one_of(map_metadata_items(),
                                keyword_metadata_items(),
                                string_metadata_items(),
                                symbol_metadata_items()))
    return metadata_item

# XXX: starting with a single metadata item, probably want to have
#      multiple eventually
@composite
def atom_vector_with_metadata_items(draw):
    n = draw(integers(min_value=0, max_value=20))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    # XXX: tweak these numbers eventually
    m = draw(integers(min_value=1, max_value=1))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "vector",
            "recipe": build_vector_with_metadata_str,
            "verify": verify_node_with_metadata,
            "metadata": md_items}
