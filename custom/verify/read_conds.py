from .verify import verify_node_as_coll, \
    verify_node_marker, \
    verify_coll_node_with_metadata

def verify(ctx, item):
    return verify_node_as_coll(ctx, item) and \
        verify_node_marker(ctx, item)

def verify_with_metadata(ctx, item):
    return verify_coll_node_with_metadata(ctx, item) and \
        verify_node_marker(ctx, item)

