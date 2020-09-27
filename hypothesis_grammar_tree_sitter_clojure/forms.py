from hypothesis.strategies import composite, one_of

# XXX: a lot more to add...
from .atoms import atom_items
from .collections import atom_collection_items

@composite
def form_items(draw):
    form_item = draw(one_of(atom_items(),
                            atom_collection_items(),
                            # XXX: more to add...
                            ))
    #
    return form_item
