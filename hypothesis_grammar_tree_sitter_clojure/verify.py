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

# (source [0, 0] - [1, 0]
#   (keyword [0, 0] - [0, 2]))

# (source [0, 0] - [1, 0]
#   (symbol [0, 0] - [0, 6]))

def verify_node_as_atom(ctx, item):
    node, source = \
        itemgetter('node', 'source')(ctx)
    label, to_str = \
        itemgetter('label', 'to_str')(item)
    assert node.type == label, \
        f'node.type != label: {node.type}, {label}'
    atom_str = to_str(item)
    text_of_node = node_text(source, node)
    assert text_of_node == atom_str, \
        f'text_of_node != atom_str: {text_of_node}, {atom_str}'
    return True

# (source [0, 0] - [1, 0]
#   (vector [0, 0] - [0, 10]
#     value: (keyword [0, 1] - [0, 3])
#     value: (keyword [0, 4] - [0, 6])
#     value: (keyword [0, 7] - [0, 9])))

def verify_node_as_coll(ctx, coll_item):
    node, source  = \
        itemgetter('node', 'source')(ctx)
    items, coll_label = \
        itemgetter('inputs', 'label')(coll_item)
    assert node.type == coll_label, \
        f'node.type != coll_label: {node.type}, {coll_label}'
    first_value_node = node.child_by_field_name("value")
    # if there was at least one value node, verify all value nodes
    if first_value_node:
        # https://github.com/tree-sitter/tree-sitter/issues/567
        cursor = node.walk() # must start at parent "containing" field
        cursor.goto_first_child()
        value_nodes = []
        if cursor.current_field_name() == "value":
            value_nodes.append(cursor.node)
        while cursor.goto_next_sibling():
            if cursor.current_field_name() == "value":
                value_nodes.append(cursor.node)
        cnt = 0
        for value_node in value_nodes:
            label, to_str = \
                itemgetter('label', 'to_str')(items[cnt])
            elt_str = to_str(items[cnt])
            assert value_node.type == label, \
                f'value_node.type != label: {value_node.type}, {label}'
            text_of_node = node_text(source, value_node)
            assert text_of_node == elt_str, \
                f'text_of_node != elt_str: {text_of_node}, {elt_str}'
            cnt += 1
        expected_cnt = len(items)
        assert expected_cnt == cnt, \
            f'expected_cnt != cnt: {expected_cnt}, {cnt}'
    return True

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
    node, source  = \
        itemgetter('node', 'source')(ctx)
    form_item, adorned_label = \
        itemgetter('inputs', 'label')(adorned_item)
    assert node.type == adorned_label, \
        f'node.type != adorned_label: {node.type}, {adorned_label}'
    # always exactly one
    form_node = node.child_by_field_name("value")
    assert form_node, \
        f'no form_node: {node.sexp()}'
    # verify there is only one value field
    cnt = 0
    # https://github.com/tree-sitter/tree-sitter/issues/567
    cursor = node.walk() # must start at parent "containing" field
    cursor.goto_first_child()
    if cursor.current_field_name() == "value":
        cnt += 1
    while cursor.goto_next_sibling():
        if cursor.current_field_name() == "value":
            cnt += 1
    assert 1 == cnt, \
        f'did not find exactly one value field: {cnt}'
    label, to_str = \
        itemgetter('label', 'to_str')(form_item)
    form_str = to_str(form_item)
    assert form_node.type == label, \
        f'form_node.type != label: {form_node.type}, {label}'
    text_of_node = node_text(source, form_node)
    assert text_of_node == form_str, \
        f'text_of_node != form_str: {text_of_node}, {form_str}'
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

# XXX: only handles one piece of metadata
#      eventually handle multiple?
def verify_node_metadata(ctx, item):
    node, source = \
        itemgetter('node', 'source')(ctx)
    md_node = node.child_by_field_name("metadata")
    assert md_node, \
      f'no metadata found: {node.sexp()}'
    mcnt = 0
    cursor = node.walk() # must start at parent "containing" field
    cursor.goto_first_child()
    if cursor.current_field_name() == "metadata":
        mcnt += 1
    while cursor.goto_next_sibling():
        if cursor.current_field_name() == "metadata":
            mcnt += 1
    assert mcnt == 1, \
      f'expected one piece of metadata, found: {mcnt}'
    # XXX: currently only one metadata item
    md_inputs, md_label, md_to_str = \
        itemgetter('inputs', 'label', 'to_str')(item["metadata"][0])
    for child in node.children:
        if child.is_named:
            # XXX: is this logic correct?
            if child.type == "metadata":
                gchildren = child.children
                n_gchildren = 0
                for gchild in gchildren:
                    if gchild.is_named:
                        n_gchildren += 1
                assert n_gchildren == 1, \
                    f'expected 1 child for metadata, found: {n_gchildren}'
                target_idx = 0
                for gchild in gchildren:
                    if gchild.is_named:
                        break
                    target_idx += 1
                target_node = gchildren[target_idx]
                assert target_node.type == md_inputs["label"], \
                   f'target_node.type != md_inputs["label"]: ' + \
                   f'{target_node.type}, {md_inputs["label"]}'
                #
                # XXX: may need to inherit metadata info too at some point?
                return md_inputs["verify"]({"node": target_node,
                                            "source": source},
                                           {"inputs": md_inputs["inputs"],
                                            "label": md_inputs["label"],
                                            "to_str": md_inputs["to_str"]})

# XXX: this only works for nodes that are collections
def verify_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

def make_single_verifier(single_name):
    def verifier(ctx, item):
        node, source = \
            itemgetter('node', 'source')(ctx)
        single_node = node.child_by_field_name(single_name)
        assert single_node, \
            f'no target single found: {node.sexp()}'
        # verify there is only one field with name single_name
        cnt = 0
        # https://github.com/tree-sitter/tree-sitter/issues/567
        cursor = node.walk() # must start at parent "containing" field
        cursor.goto_first_child()
        if cursor.current_field_name() == single_name:
            cnt += 1
        while cursor.goto_next_sibling():
            if cursor.current_field_name() == single_name:
                cnt += 1
        assert 1 == cnt, \
            f'expected exactly one field named {single_name}, found: {cnt}'
        single_item = item[single_name]
        single_inputs, single_label, single_to_str = \
            itemgetter('inputs', 'label', 'to_str')(single_item)
        assert single_node.type == single_label, \
            f'single_node.type != single_label: ' + \
            f'{single_node.type}, {single_label}'
        #
        return single_item["verify"]({"node": single_node,
                                      "source": source},
                                     single_item)
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
def verify_node_as_form(ctx, item):
    return True

# XXX: incomplete
def verify_node_leads_with(ctx, item):
    return True

def verify_node_as_discard_expr(ctx, item):
    return verify_node_leads_with(ctx, item) and \
        verify_node_as_form(ctx, item)
