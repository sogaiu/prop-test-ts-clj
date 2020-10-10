from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll, \
    verify_coll_node_with_metadata

from .util import make_form_with_metadata_str_builder

# list: $ =>
#   seq(repeat($._metadata),
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
def list_items(draw, elements):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements, min_size=0, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": items,
            "label": "list",
            "to_str": build_list_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def number_list_items(draw):
    number_list_item = draw(list_items(elements=number_items()))
    #
    return number_list_item

@composite
def atom_list_items(draw):
    atom_list_item = draw(list_items(elements=atom_items()))
    #
    return atom_list_item

# XXX: generic list at some point?
@composite
def atom_list_with_metadata_items(draw):
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
    str_builder = make_form_with_metadata_str_builder(build_list_str)
    #
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "list",
            "to_str": str_builder,
            "verify": verify_coll_node_with_metadata,
            "metadata": md_items,
            "separators": sep_strs}
