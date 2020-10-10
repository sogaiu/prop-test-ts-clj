from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll, \
    verify_coll_node_with_metadata

from .util import make_form_with_metadata_str_builder

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
def set_items(draw, elements):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": items,
            "label": "set",
            "to_str": build_set_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def number_set_items(draw):
    number_set_item = draw(set_items(elements=number_items()))
    #
    return number_set_item

@composite
def atom_set_items(draw):
    atom_set_item = draw(set_items(elements=atom_items()))
    #
    return atom_set_item

# XXX: generic set at some point?
@composite
def atom_set_with_metadata_items(draw):
    # avoid circular dependency
    from .metadata import metadata_items
    #
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    atm_items = draw(lists(elements=atom_items(),
                           min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    str_builder = make_form_with_metadata_str_builder(build_set_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "set",
            "to_str": str_builder,
            "verify": verify_coll_node_with_metadata,
            "metadata": md_items,
            "separators": sep_strs}
