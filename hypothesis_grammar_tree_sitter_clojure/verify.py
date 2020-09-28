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
    label, recipe = \
        itemgetter('label', 'recipe')(item)
    if node.type != label:
        # XXX
        print("node type mismatch")
        print("  node:", node.type)
        print("  expected:", label)
        return False
    atom_str = recipe(item)
    text_of_node = node_text(source, node)
    if text_of_node != atom_str:
        # XXX
        print("node text mismatch")
        print("  node:", text_of_node)
        print("  expected:", atom_str)
        return False
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
    if node.type != coll_label:
        # XXX
        print("node type mismatch")
        print("  node:", node.type)
        print("  expected:", coll_label)
        return False
    first_value_node = node.child_by_field_name("value")
    n_children = len(node.children)
    # if there was at least one value node, verify all value nodes
    if first_value_node:
        cnt = 0
        # find the index of the value node just found
        while (cnt < n_children):
            # must succeed given definition of first_value_node
            if first_value_node == node.children[cnt]:
                break
            cnt += 1
        first_value_node_idx = cnt
        value_node_cnt = 0
        # start verifying from first value node
        for idx in range(first_value_node_idx, n_children):
            child = node.children[idx]
            # assumes that after first value node, all named nodes are
            # value nodes (node which is associated with field "value")
            if child.is_named:
                label, recipe = \
                    itemgetter('label', 'recipe')(items[value_node_cnt])
                elt_str = recipe(items[value_node_cnt])
                if child.type != label:
                    # XXX
                    print("node type mismatch")
                    print("  node:", node.type)
                    print("  expected:", label)
                    return False
                text_of_node = node_text(source, child)
                if text_of_node != elt_str:
                    # XXX
                    print("node text mismatch")
                    print("  node:", text_of_node)
                    print("  expected:", elt_str)
                    return False
                value_node_cnt += 1
        expected_cnt = len(items)
        if expected_cnt != value_node_cnt:
            # XXX
            print("unexpected number of element nodes")
            print("  actual:", child_cnt)
            print("  expected:", expected_cnt)
            return False
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
    if node.type != adorned_label:
        # XXX
        print("node type mismatch")
        print("  node:", node.type)
        print("  expected:", adorned_label)
        return False
    # always exactly one
    form_node = node.child_by_field_name("value")
    if not form_node:
        # XXX
        print("did not find value field")
        print("  node:", node.sexp())
        return False
    # XXX: this test doesn't seem doable w/ py-tree-sitter atm
    #      goal is to verify there is only one value field,
    #      but the cursor api doesn't seem to work from an
    #      arbitrary node
    # cnt = 0
    # cursor = form_node.walk()
    #
    # XXX: code here for visiting all children, counting
    #      nodes that correspond to the field "value"
    #
    # if 1 != cnt:
    #     # XXX
    #     print("did not find exactly one value field")
    #     print("  cnt:", cnt)
    #     return False
    label, recipe = \
        itemgetter('label', 'recipe')(form_item)
    form_str = recipe(form_item)
    if form_node.type != label:
        # XXX
        print("node type mismatch")
        print("  node:", form_node.type)
        print("  expected:", label)
        return False
    text_of_node = node_text(source, form_node)
    if text_of_node != form_str:
        # XXX
        print("node text mismatch")
        print("  node:", text_of_node)
        print("  expected:", form_str)
        return False
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
    if md_node == None:
        # XXX
        print("no metadata found")
        return False
    mcnt = 0
    for child in node.children:
        if child.type == "metadata":
            mcnt += 1
    if mcnt > 1:
        # XXX
        print("more than one piece of metadata found")
        return False
    # XXX: currently only one metadata item
    md_inputs, md_label, md_recipe = \
        itemgetter('inputs', 'label', 'recipe')(item["metadata"][0])
    for child in node.children:
        if child.is_named:
            # XXX: is this logic correct?
            if child.type == "metadata":
                gchildren = child.children
                n_gchildren = 0
                for gchild in gchildren:
                    if gchild.is_named:
                        n_gchildren += 1
                if n_gchildren != 1:
                    # XXX
                    print("metadata doesn't have exactly 1 child")
                    print(n_gchildren)
                    return False
                target_idx = 0
                for gchild in gchildren:
                    if gchild.is_named:
                        break
                    target_idx += 1
                target_node = gchildren[target_idx]
                if target_node.type != md_inputs["label"]:
                    # XXX
                    print("metadata child node type mismatch")
                    print("  node:", target_node.type)
                    print("  expected:", md_inputs["label"])
                    return False
                #
                # XXX: may need to inherit metadata info too at some point?
                return md_inputs["verify"]({"node": target_node,
                                            "source": source},
                                           {"inputs": md_inputs["inputs"],
                                            "label": md_inputs["label"],
                                            "recipe": md_inputs["recipe"]})

# XXX: this only works for nodes that are collections
def verify_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)
