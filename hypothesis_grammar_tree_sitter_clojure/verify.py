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

def verify_node_type_and_text(ctx, item):
    return verify_node_type(ctx, item) and \
        verify_node_text(ctx, item)

def verify_node_as_atom(ctx, item):
    return verify_node_type(ctx, item) and \
        verify_node_text(ctx, item)

def verify_node_as_coll(ctx, coll_item):
    node, source = itemgetter('node', 'source')(ctx)
    items = itemgetter('inputs')(coll_item)
    verify_node_type(ctx, coll_item)
    first_value_node = node.child_by_field_name("value")
    # if there was at least one value node, verify all value nodes
    if first_value_node:
        value_nodes = child_nodes_with_field_name(node, "value")
        n_value_nodes = len(value_nodes)
        assert len(items) == n_value_nodes, \
            f'expected: {len(items)} node(s), got: {n_value_nodes}'
        for idx in range(0, n_value_nodes):
            verify_node_type_and_text({"node": value_nodes[idx],
                                       "source": source},
                                      items[idx])
    return True

# XXX: essentially same as verify_node_as_atom...
def verify_node_as_form(ctx, form_item):
    return verify_node_type(ctx, form_item) and \
        verify_node_text(ctx, form_item)

def verify_node_as_adorned(ctx, adorned_item):
    node, source = itemgetter('node', 'source')(ctx)
    form_item, adorned_label = itemgetter('inputs', 'label')(adorned_item)
    verify_node_type(ctx, adorned_item)
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


def verify_node_metadata(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    md_node = node.child_by_field_name("metadata")
    assert md_node, \
      f'no metadata found: {node.sexp()}'
    md_nodes = child_nodes_with_field_name(node, "metadata")
    n_md_nodes = len(md_nodes)
    md_items = item["metadata"]
    assert len(md_items) == n_md_nodes, \
        f'expected {len(md_items)} metadata nodes, got: {n_md_nodes}'
    # XXX: could probably be improved for clarity
    for idx in range(0, n_md_nodes):
        md_item = md_items[idx]
        md_node = md_nodes[idx]
        assert md_node.type == "metadata"
        assert md_node.named_child_count == 1
        inner_item = md_item["inputs"]
        assert inner_item
        inner_node = md_node.child_by_field_name("value")
        assert inner_node
        inner_item["verify"]({"node": inner_node,
                              "source": source},
                             inner_item)
    return True

# XXX: this only works for nodes that are collections
def verify_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

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

verify_node_prefix = make_single_verifier("prefix")

def verify_node_with_prefix(ctx, item):
    return verify_node_prefix(ctx, item) and \
        verify_node_as_coll(ctx, item)

verify_node_tag = make_single_verifier("tag")

# XXX: possibly want to change verify_node_as_adorned
#      to have a different name or split out common functionality
def verify_node_with_tag(ctx, item):
    return verify_node_tag(ctx, item) and \
        verify_node_as_adorned(ctx, item)

# XXX: incomplete
def verify_node_leads_with(ctx, item):
    return True

def verify_node_as_discard_expr(ctx, item):
    return verify_node_leads_with(ctx, item) and \
        verify_node_as_form(ctx, item)
