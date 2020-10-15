from .verify import verify_node_as_adorned, \
    make_single_verifier, \
    verify_node_metadata

def verify(ctx, item):
    return make_single_verifier("tag")(ctx, item) and \
        verify_node_as_adorned(ctx, item)

def verify_with_metadata(ctx, item):
    return make_single_verifier("tag")(ctx, item) and \
        verify_node_as_adorned(ctx, item) and \
        verify_node_metadata(ctx, item)
