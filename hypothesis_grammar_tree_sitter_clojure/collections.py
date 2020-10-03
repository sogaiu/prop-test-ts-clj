from hypothesis.strategies import composite, one_of

# XXX: does it make sense to do generic collections at some point?
# XXX: any other things?
from .lists import atom_list_items
from .maps import atom_map_items
from .namespaced_maps import atom_namespaced_map_items
from .sets import atom_set_items
from .vectors import atom_vector_items

@composite
def atom_collection_items(draw):
    atom_collection_item = draw(one_of(atom_list_items(),
                                       atom_map_items(),
                                       atom_namespaced_map_items(),
                                       atom_set_items(),
                                       atom_vector_items()))
    return atom_collection_item
