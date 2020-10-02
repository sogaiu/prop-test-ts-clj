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

# (source [0, 0] - [1, 0]
#   (keyword [0, 0] - [0, 2]))

# (source [0, 0] - [1, 0]
#   (symbol [0, 0] - [0, 6]))

def verify_node_as_atom(ctx, item):
    return verify_node_type(ctx, item) and \
        verify_node_text(ctx, item)

# (source [0, 0] - [1, 0]
#   (vector [0, 0] - [0, 10]
#     value: (keyword [0, 1] - [0, 3])
#     value: (keyword [0, 4] - [0, 6])
#     value: (keyword [0, 7] - [0, 9])))

def verify_node_as_coll(ctx, coll_item):
    node, source  = itemgetter('node', 'source')(ctx)
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

# (source [0, 0] - [1, 0]
#  (quote_form [0, 0] - [0, 12]
#    value: (symbol [0, 1] - [0, 12])))

# (source [0, 0] - [1, 0]
#   (quote_form [0, 0] - [0, 19]
#     value: (list [0, 1] - [0, 19]
#       value: (symbol [0, 2] - [0, 6])
#       value: (symbol [0, 7] - [0, 13])
#       value: (symbol [0, 14] - [0, 18]))))

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

# XXX: note that there is no value field for this case,
#      but for all(?) other cases there is
#
# (source [0, 0] - [1, 0]
#   (symbol [0, 0] - [0, 12]
#     metadata: (metadata [0, 0] - [0, 5]
#       (keyword [0, 1] - [0, 5]))))

# (source [0, 0] - [1, 0]
#   (vector [0, 0] - [0, 12]
#     metadata: (metadata [0, 0] - [0, 7]
#       (map [0, 1] - [0, 7]
#         value: (keyword [0, 2] - [0, 4])
#         value: (number [0, 5] - [0, 6])))
#     value: (keyword [0, 9] - [0, 11])))

# (source [0, 0] - [1, 0]
#   (quote_form [0, 0] - [0, 14]
#     metadata: (metadata [0, 0] - [0, 5]
#       (keyword [0, 1] - [0, 5]))
#     value: (vector [0, 7] - [0, 14]
#       value: (keyword [0, 8] - [0, 10])
#       value: (keyword [0, 11] - [0, 13]))))

# (source [0, 0] - [1, 0]
#   (quote_form [0, 0] - [0, 10]
#     metadata: (metadata [0, 0] - [0, 5]
#       (keyword [0, 1] - [0, 5]))
#     value: (symbol [0, 7] - [0, 10])))

# once a node with field "metadata" is found:

# (metadata [0, 0] - [0, 7]
#   (map [0, 1] - [0, 7]
#     value: (keyword [0, 2] - [0, 4])
#     value: (number [0, 5] - [0, 6])))

# (metadata [0, 0] - [0, 5]
#   (keyword [0, 1] - [0, 5]))

def verify_node_metadata(ctx, item):
    node, source = itemgetter('node', 'source')(ctx)
    md_node = node.child_by_field_name("metadata")
    assert md_node, \
      f'no metadata found: {node.sexp()}'
    md_nodes = child_nodes_with_field_name(node, "metadata")
    n_md_nodes = len(md_nodes)
    md_items = item["metadata"]
    assert n_md_nodes == len(md_items), \
        f'expected {len(md_items)} metadata nodes, got: {n_md_nodes}'
    # XXX: could probably be improved for clarity
    for idx in range(0, n_md_nodes):
        md_item = md_items[idx]
        md_node = md_nodes[idx]
        assert md_node.type == "metadata"
        assert md_node.named_child_count == 1
        md_item["verify"]({"node": md_node,
                           "source": source},
                          md_item)
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

# #::{}
#
# (source [0, 0] - [1, 0]
#   (namespaced_map [0, 0] - [0, 5]
#     prefix: (auto_res_marker [0, 1] - [0, 3])))

# #::{:a 1}
#
# (source [0, 0] - [1, 0]
#   (namespaced_map [0, 0] - [0, 9]
#     prefix: (auto_res_marker [0, 1] - [0, 3])
#     value: (keyword [0, 4] - [0, 6])
#     value: (number [0, 7] - [0, 8])))

# #:hello{}
#
# (source [0, 0] - [1, 0]
#   (namespaced_map [0, 0] - [0, 9]
#     prefix: (keyword [0, 1] - [0, 7])))

# #:hello{:a 1}

# (source [0, 0] - [1, 0]
#   (namespaced_map [0, 0] - [0, 13]
#     prefix: (keyword [0, 1] - [0, 7])
#     value: (keyword [0, 8] - [0, 10])
#     value: (number [0, 11] - [0, 12])))

# #:hello/there{:a 1}
#
# (source [0, 0] - [1, 0]
#   (namespaced_map [0, 0] - [0, 19]
#     prefix: (keyword [0, 1] - [0, 13])
#     value: (keyword [0, 14] - [0, 16])
#     value: (number [0, 17] - [0, 18])))

verify_node_prefix = make_single_verifier("prefix")

def verify_node_with_prefix(ctx, item):
    return verify_node_prefix(ctx, item) and \
        verify_node_as_coll(ctx, item)

# (source [0, 0] - [1, 0]
#   (tagged_literal [0, 0] - [0, 44]
#     tag: (symbol [0, 1] - [0, 5])
#     value: (string [0, 6] - [0, 44])))

verify_node_tag = make_single_verifier("tag")

# XXX: possibly want to change verify_node_as_adorned
#      to have a different name or split out common functionality
def verify_node_with_tag(ctx, item):
    return verify_node_tag(ctx, item) and \
        verify_node_as_adorned(ctx, item)

# XXX: incomplete
#def verify_node_as_form(ctx, item):
#    return True

# XXX: incomplete
def verify_node_leads_with(ctx, item):
    return True

# (source [0, 0] - [1, 0]
#   (discard_expr [0, 0] - [0, 4]
#     value: (number [0, 3] - [0, 4])))

def verify_node_as_discard_expr(ctx, item):
    return verify_node_leads_with(ctx, item) and \
        verify_node_as_form(ctx, item)
