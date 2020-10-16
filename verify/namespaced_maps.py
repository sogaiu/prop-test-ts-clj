from .verify import verify_node_as_coll, \
    verify_coll_node_with_metadata, \
    make_single_verifier

def verify(ctx, item):
    return make_single_verifier("prefix")(ctx, item) and \
        verify_node_as_coll(ctx, item)

def verify_with_metadata(ctx, item):
    return make_single_verifier("prefix")(ctx, item) and \
        verify_coll_node_with_metadata(ctx, item)
