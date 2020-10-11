from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll, \
    verify_coll_node_with_metadata

from .util import make_form_with_metadata_str_builder

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

# XXX: possibly make form_items be the default for elements?
@composite
def map_items(draw, elements, metadata=False):
    # avoid circular dependency
    from .metadata import metadata_items, check_metadata_param
    #
    check_metadata_param(metadata)
    # XXX: what about this /2?
    n = 2 * draw(integers(min_value=0, max_value=coll_max/2))
    #
    items = draw(lists(elements=elements, min_size=n, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    if not metadata:
        return {"inputs": items,
                "label": "map",
                "to_str": build_map_str,
                "verify": verify_node_as_coll,
                "separators": sep_strs}
    else:
        str_builder = make_form_with_metadata_str_builder(build_map_str)
        #
        m = draw(integers(min_value=1, max_value=metadata_max))
        #
        md_items = draw(lists(elements=metadata_items(),
                              min_size=m, max_size=m))
        #
        return {"inputs": items,
                "label": "map",
                "to_str": str_builder,
                "verify": verify_coll_node_with_metadata,
                "metadata": md_items,
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
