from operator import itemgetter

# XXX: at one point had trouble with: \Ā
#      this turned out to be a bug with node_text --
#      wasn't encoding and decoding to / from bytes --
#      tree-sitter gives locations as bytes, so that's necessary
#
# assume here that source is a utf8 string
def node_text(source, node):
    return \
        bytes(source, "utf8")[node.start_byte:node.end_byte].decode("utf-8")

def child_nodes_with_field_name(node, name):
    cursor = node.walk()
    cursor.goto_first_child()
    value_nodes = []
    if cursor.current_field_name() == name:
        value_nodes.append(cursor.node)
    while cursor.goto_next_sibling():
        if cursor.current_field_name() == name:
            value_nodes.append(cursor.node)
    return value_nodes

def child_nodes_with_field_names(node, names):
    cursor = node.walk()
    cursor.goto_first_child()
    value_nodes = []
    if cursor.current_field_name() in names:
        value_nodes.append(cursor.node)
        while cursor.goto_next_sibling():
            if cursor.current_field_name() in names:
                value_nodes.append(cursor.node)
    return value_nodes

def verify_node_type(ctx, item):
    node = itemgetter('node')(ctx)
    label = itemgetter('label')(item)
    assert node.type == label, \
        f'expected node type: {node.type}, got: {label}'
    return True

def verify_node_text(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    to_str = itemgetter('to_str')(item)
    as_str = to_str(item)
    text_of_node = node_text(source, node)
    assert text_of_node == as_str, \
        f'expected node text: {text_of_node}, got: {as_str}'
    return True

def verify_node_no_error(ctx):
    assert not ctx["node"].has_error
    return True

def verify_node_marker(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    marker = item["marker"]
    marker_node = node.child_by_field_name("marker")
    assert marker_node, \
        f'did not find marker node: {source}'
    text_of_node = node_text(source, marker_node)
    assert text_of_node == marker, \
        f'expected marker: {marker}, got: {text_of_node}'
    return True

# XXX: additional possibilities for verification:
#
#        open delimiter node comes before close delimiter node
#        open delimiter node comes after all metadata (if any)
#        open delimiter node comes before all value nodes (if any)
def verify_node_delimiters(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    open_delim, close_delim = itemgetter('open', 'close')(item)
    actual_open = node_text(source, node.child_by_field_name('open'))
    assert open_delim == actual_open, \
        f'expected open delimiter: {open_delim}, got: {actual_open}'
    close_node = node.child_by_field_name('close')
    actual_close = node_text(source, close_node)
    assert close_delim == actual_close, \
        f'expected close delimiter: {close_delim}, got: {actual_close}'
    assert node.children[-1] == close_node, \
        f'node for closing delimiter was not last child node'
    return True

def verify_node_type_text_and_no_error(ctx, item):
    return verify_node_no_error(ctx) and \
        verify_node_type(ctx, item) and \
        verify_node_text(ctx, item)

def verify_node_as_atom(ctx, item):
    return verify_node_no_error(ctx) and \
        verify_node_type(ctx, item) and \
        verify_node_text(ctx, item)

def verify_node_as_coll(ctx, coll_item):
    node, source = itemgetter('node', 'source')(ctx)
    verify_node_no_error(ctx)
    items = itemgetter('inputs')(coll_item)
    verify_node_type(ctx, coll_item)
    verify_node_delimiters(ctx, coll_item)
    verify_node_text(ctx, coll_item)
    first_value_node = node.child_by_field_name("value")
    # if there was at least one value node, verify all value nodes
    if first_value_node:
        value_nodes = child_nodes_with_field_name(node, "value")
        n_value_nodes = len(value_nodes)
        assert len(items) == n_value_nodes, \
            f'expected: {len(items)} node(s), got: {n_value_nodes}'
        for idx in range(0, n_value_nodes):
            verify_node_type_text_and_no_error({"node": value_nodes[idx],
                                                "source": source},
                                               items[idx])
    return True

# XXX: essentially same as verify_node_as_atom...
def verify_node_as_form(ctx, form_item):
    return verify_node_no_error(ctx) and \
        verify_node_type(ctx, form_item) and \
        verify_node_text(ctx, form_item)

def verify_node_as_adorned(ctx, adorned_item):
    node, source = itemgetter('node', 'source')(ctx)
    form_item, adorned_label = itemgetter('inputs', 'label')(adorned_item)
    verify_node_type(ctx, adorned_item)
    verify_node_marker(ctx, adorned_item)
    # verify there is only one value field
    cnt = len(child_nodes_with_field_name(node, "value"))
    assert 1 == cnt, \
        f'expected 1 value field, got: {cnt}'
    # must succeed given previous lines
    form_node = node.child_by_field_name("value")
    verify_node_as_form({"node": form_node,
                         "source": source},
                        form_item)
    return True

def verify_node_metadatum(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    verify_node_no_error(ctx)
    verify_node_type(ctx, item)
    verify_node_marker(ctx, item)
    assert node.named_child_count == 1
    inner_item = item["inputs"]
    assert inner_item
    inner_node = node.child_by_field_name("value")
    assert inner_node
    inner_item["verify"]({"node": inner_node,
                          "source": source},
                         inner_item)
    return True

def verify_node_metadata(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    md_nodes = child_nodes_with_field_names(node, ["meta", "old_meta"])
    n_md_nodes = len(md_nodes)
    md_items = item["metadata"]
    assert len(md_items) == n_md_nodes, \
        f'expected {len(md_items)} metadata nodes, got: {n_md_nodes}'
    for idx in range(0, n_md_nodes):
        verify_node_metadatum({"node": md_nodes[idx],
                               "source": source},
                              md_items[idx])
    return True

def verify_coll_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

def verify_adorned_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_adorned(ctx, item)

# examples of single_name:
#
# * prefix
# * tag
def make_single_verifier(single_name):
    def verifier(ctx, item):
        node, source = itemgetter('node', 'source')(ctx)
        single_node = node.child_by_field_name(single_name)
        assert single_node, \
            f'no field with name: {single_name} for: {node.sexp()}'
        # verify there is only one field with name single_name
        cnt = len(child_nodes_with_field_name(node, single_name))
        assert 1 == cnt, \
            f'expected exactly one field named {single_name}, got: {cnt}'
        single_item = item[single_name]
        single_ctx = {"node": single_node,
                      "source": source}
        verify_node_type(single_ctx, single_item)
        # XXX: doesn't the following line include the previous line?
        return single_item["verify"](single_ctx, single_item)
    return verifier
