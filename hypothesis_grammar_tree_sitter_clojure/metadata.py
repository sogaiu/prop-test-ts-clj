from hypothesis.strategies import integers
from hypothesis.strategies import composite, just, one_of

from .keywords import unqualified_keyword_items, \
    qualified_keyword_items
# XXX: want generic (i.e. not just atoms) map_items eventually?
from .maps import atom_map_items
from .read_conds import read_cond_items
from .strings import string_items
from .symbols import symbol_items
# metadatee-related (maps and symbols from above would be too)
from .atoms import atom_items

from .separators import separator_strings

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

# old_metadata: $ =>
#   seq("#^",
#       repeat($._non_form),
#       field('value', choice($.read_cond,
#                             $.map,
#                             $.string,
#                             $.keyword,
#                             $.symbol))),

marker_for_label = \
    {"metadata": "^",
     "old_metadata": '#^'}

# XXX: there is one separator of interest and that is potentially
#      between ^ / #^ and the rest of the form.  the default here is
#      no separator.
def build_metadata_str(md_item):
    inner_item = md_item["inputs"]
    #
    marker = md_item["marker"]
    body_str = inner_item["to_str"](inner_item)
    #
    return f'{marker}{body_str}'

def attach_metadata(metadata_strs, metadatee_str):
    # XXX: another "what to do about separator" location
    return " ".join(metadata_strs + [metadatee_str])

# XXX: only non-auto-resolved-keywords are valid
@composite
def keyword_metadata_items(draw, label="metadata"):
    keyword_item = draw(one_of(unqualified_keyword_items(),
                               qualified_keyword_items()))
    #
    return {"inputs": keyword_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom,
            "marker": marker_for_label[label]}

@composite
def map_metadata_items(draw, label="metadata"):
    # XXX: needs generalization?
    map_item = draw(atom_map_items())
    #
    return {"inputs": map_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_node_as_coll,
            "marker": marker_for_label[label]}

@composite
def read_cond_metadata_items(draw, label="metadata"):
    read_cond_item = draw(read_cond_items())
    #
    return {"inputs": read_cond_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_node_as_coll,
            "marker": marker_for_label[label]}

@composite
def string_metadata_items(draw, label="metadata"):
    string_item = draw(string_items())
    #
    return {"inputs": string_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom,
            "marker": marker_for_label[label]}

@composite
def symbol_metadata_items(draw, label="metadata"):
    symbol_item = draw(symbol_items())
    #
    return {"inputs": symbol_item,
            "label": label,
            "to_str": build_metadata_str,
            "verify": verify_node_as_atom,
            "marker": marker_for_label[label]}

@composite
def metadata_items(draw, label="metadata"):
    if label == "any":
        label = draw(one_of(just("metadata"),
                            just("old_metadata")))
    #
    assert label in ["metadata", "old_metadata"], \
        f'unexpected label value: {label}'
    #
    metadata_item = \
        draw(one_of(map_metadata_items(label=label),
                    keyword_metadata_items(label=label),
                    read_cond_metadata_items(label=label),
                    string_metadata_items(label=label),
                    symbol_metadata_items(label=label)))
    return metadata_item

def check_metadata_param(metadata):
    assert metadata in ["any", "metadata", "old_metadata", False, None], \
        f'unexepected metadata specifier: {metadata}'
