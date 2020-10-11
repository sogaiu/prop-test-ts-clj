from hypothesis.strategies import integers
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

from .separators import separator_strings

# XXX: clean up later
from .verify import verify_node_as_atom, \
    verify_node_as_coll

# metadata: $ =>
#   seq("^",
#       repeat($._non_form),
#       field('value', choice($.read_cond,
#                             $.map,
#                             $.string,
#                             $.keyword,
#                             $.symbol))),

# XXX: there is one separator of interest and that is potentially
#      between ^ and the rest of the form.  the default here is
#      no separator.
def build_metadata_str(md_item):
    inner_item = md_item["inputs"]
    return f'^{inner_item["to_str"](inner_item)}'

def attach_metadata(metadata_strs, metadatee_str):
    # XXX: another "what to do about separator" location
    return " ".join(metadata_strs + [metadatee_str])

# XXX: only non-auto-resolved-keywords are valid
@composite
def keyword_metadata_items(draw):
    keyword_item = draw(one_of(unqualified_keyword_items(),
                               qualified_keyword_items()))
    #
    return {"inputs": keyword_item,
            "label": "metadata",
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom}

@composite
def map_metadata_items(draw):
    # XXX: needs generalization?
    map_item = draw(atom_map_items())
    #
    return {"inputs": map_item,
            "label": "metadata",
            "to_str": build_metadata_str,
            "verify": verify_node_as_coll}

@composite
def string_metadata_items(draw):
    string_item = draw(string_items())
    #
    return {"inputs": string_item,
            "label": "metadata",
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom}

@composite
def symbol_metadata_items(draw):
    symbol_item = draw(symbol_items())
    #
    return {"inputs": symbol_item,
            "label": "metadata",
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom}

@composite
def metadata_items(draw):
    metadata_item = draw(one_of(map_metadata_items(),
                                keyword_metadata_items(),
                                string_metadata_items(),
                                symbol_metadata_items()))
    return metadata_item
