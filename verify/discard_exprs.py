from .verify import verify_node_marker, \
    verify_node_as_form

def verify(ctx, item):
    return verify_node_marker(ctx, item) and \
        verify_node_as_form(ctx, item)
