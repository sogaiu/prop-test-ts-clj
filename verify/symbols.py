from .verify import verify_node_as_atom, \
    verify_node_metadata

verify = verify_node_as_atom

def verify_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_atom(ctx, item)
