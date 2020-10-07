from hypothesis import assume

from hypothesis.strategies import composite, one_of, recursive

from .atoms import atom_items

from .lists import atom_list_items, \
    list_items
from .maps import atom_map_items, \
    map_items
from .namespaced_maps import atom_namespaced_map_items, \
    namespaced_map_items
from .sets import atom_set_items, \
    set_items
from .vectors import atom_vector_items, \
    vector_items

@composite
def atom_collection_items(draw):
    atom_collection_item = draw(one_of(atom_list_items(),
                                       atom_map_items(),
                                       atom_namespaced_map_items(),
                                       atom_set_items(),
                                       atom_vector_items()))
    return atom_collection_item

@composite
def collection_items(draw, elements):
    coll_item = draw(one_of(list_items(elements),
                            map_items(elements),
                            namespaced_map_items(elements),
                            vector_items(elements),
                            set_items(elements)))
    return coll_item

@composite
def recursive_collection_items(draw):
    rec_coll_item = draw(recursive(atom_items(), collection_items))
    # XXX: without this seems to test too many degenerate cases?
    assume(len(rec_coll_item["inputs"]) > 0)
    #
    return rec_coll_item
