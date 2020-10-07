from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from .parameters import coll_max, metadata_max

from .atoms import atom_items
from .numbers import number_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# vector: $ =>
#   seq(repeat($._metadata),
#       $._bare_vector),
#
# _bare_vector: $ =>
#   seq("[",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       "]"),

# XXX: could also have stuff before and after delimiters
def build_vector_str(vector_item):
    items = vector_item["inputs"]
    seps = vector_item["separators"]
    vector_elts = []
    for i, s in zip(items, seps):
        vector_elts += i["to_str"](i) + s
    return "[" + "".join(vector_elts) + "]"

@composite
def vector_items(draw, elements):
    n = draw(integers(min_value=0, max_value=coll_max))
    #
    items = draw(lists(elements, min_size=0, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=n, max_size=n))
    #
    return {"inputs": items,
            "label": "vector",
            "to_str": build_vector_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs}

@composite
def number_vector_items(draw):
    number_vector_item = draw(vector_items(elements=number_items()))
    #
    return number_vector_item

@composite
def atom_vector_items(draw):
    atom_vector_item = draw(vector_items(elements=atom_items()))
    #
    return atom_vector_item

def build_vector_with_metadata_str(item):
    # avoid circular dependency
    from .metadata import attach_metadata
    #
    vec_str = build_vector_str(item)
    #
    md_items = item["metadata"]
    md_item_strs = [md_item["to_str"](md_item) for md_item in md_items]
    #
    return attach_metadata(md_item_strs, vec_str)

def verify_coll_node_with_metadata(ctx, item):
    # avoid circular dependency
    from .verify import verify_node_metadata
    #
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

@composite
def atom_vector_with_metadata_items(draw):
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
    m = draw(integers(min_value=1, max_value=metadata_max))
    #
    md_items = draw(lists(elements=metadata_items(),
                          min_size=m, max_size=m))
    #
    return {"inputs": atm_items,
            "label": "vector",
            "to_str": build_vector_with_metadata_str,
            "verify": verify_coll_node_with_metadata,
            "metadata": md_items,
            "separators": sep_strs}
