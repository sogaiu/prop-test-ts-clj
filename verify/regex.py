from .verify import verify_node_type_text_and_no_error, \
    verify_node_marker

def verify(ctx, item):
    return verify_node_type_text_and_no_error(ctx, item) and \
        verify_node_marker(ctx, item)
