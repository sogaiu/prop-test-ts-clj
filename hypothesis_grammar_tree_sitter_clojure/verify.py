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
    cnt = 0
    for child in node.children:
        if child.is_named:
            # XXX: is this logic correct?
            if child.type == "metadata":
                pass
            else:
                label, recipe = \
                    itemgetter('label', 'recipe')(items[cnt])
                coll_str = recipe(items[cnt])
                if child.type != label:
                    # XXX
                    print("node type mismatch")
                    print("  node:", node.type)
                    print("  expected:", label)
                    return False
                text_of_node = node_text(source, child)
                if text_of_node != coll_str:
                    # XXX
                    print("node text mismatch")
                    print("  node:", text_of_node)
                    print("  expected:", coll_str)
                    return False
                cnt += 1
    expected_cnt = len(items)
    if expected_cnt != cnt:
        # XXX
        print("unexpected number of element nodes")
        print("  actual:", cnt)
        print("  expected:", expected_cnt)
        return False
    else:
        return True

# XXX: only handles one pieces of metadata
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

def verify_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

