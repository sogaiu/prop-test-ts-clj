# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file
from operator import itemgetter

from hypothesis import given
from hypothesis import note, settings, Verbosity

# XXX: clean this up later
from hypothesis_grammar_tree_sitter_clojure.characters import *
from hypothesis_grammar_tree_sitter_clojure.keywords import *
from hypothesis_grammar_tree_sitter_clojure.numbers import *
from hypothesis_grammar_tree_sitter_clojure.strings import *
from hypothesis_grammar_tree_sitter_clojure.symbols import *
#
from hypothesis_grammar_tree_sitter_clojure.lists import *
from hypothesis_grammar_tree_sitter_clojure.maps import *
from hypothesis_grammar_tree_sitter_clojure.vectors import *
#
from hypothesis_grammar_tree_sitter_clojure.metadata import *

vb = Verbosity.verbose
#vb = Verbosity.normal

from tree_sitter import Language, Parser

# may need to create build subdir...
so_with_langs_path = 'build/my-languages.so'

Language.build_library(
    so_with_langs_path,
    ['vendor/tree-sitter-clojure']
)

CLJ_LANGUAGE = Language(so_with_langs_path, 'clojure')

parser = Parser()
parser.set_language(CLJ_LANGUAGE)

# XXX: at one point had trouble with: \Ā
#      this turned out to be a bug with node_text --
#      wasn't encoding and decoding to / from bytes --
#      tree-sitter gives locations as bytes, so that's necessary
#
# assume here that source is a utf8 string
def node_text(source, node):
    return bytes(source, "utf8")[node.start_byte:node.end_byte].decode("utf-8")

def get_lone_node(form_str):
    tree = parser.parse(bytes(form_str, "utf8"))
    root_node = tree.root_node
    children = root_node.children
    n_children = len(children)
    if n_children != 1:
        # XXX
        print("did not find exactly 1 child")
        print("  n_children:", n_children)
        print("  form_str:", form_str)
        for child in children:
           print(f'  {child}')
           print(f'  {child.sexp()}')
    assert 1 == n_children
    return children[0]

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
                return verify_node({"node": target_node,
                                    "source": source},
                                   {"inputs": md_inputs["inputs"],
                                    "label": md_inputs["label"],
                                    "recipe": md_inputs["recipe"]})

def verify_node_with_metadata(ctx, item):
    return verify_node_metadata(ctx, item) and \
        verify_node_as_coll(ctx, item)

def has_metadata(item):
    return "metadata" in item

def is_atom(item):
    # XXX: update this list when necessary
    return item["label"] in [#"boolean",
                             "character",
                             "keyword",
                             #"nil",
                             "number",
                             "string",
                             "symbol"]

def is_coll(item):
    # XXX: update this list when necessary
    return item["label"] in ["list",
                             "map",
                             #"namespaced_map",
                             "vector",
                             "set"]

def verify_node(ctx, item):
    # XXX: any way to avoid this kind of conditional?
    if has_metadata(item):
        return verify_node_with_metadata(ctx, item)
    elif is_atom(item):
        return verify_node_as_atom(ctx, item)
    elif is_coll(item):
        return verify_node_as_coll(ctx, item)
    else:
        # XXX
        print("unexpected item:", item)
        return False

def form_test(item):
    form_str = item["recipe"](item)
    ctx = {"node": get_lone_node(form_str),
           "source": form_str}
    assert verify_node(ctx, item)

## numbers

@settings(verbosity=vb)
@given(hex_number_items())
def test_parses_hex_as_number(hex_num_item):
    form_test(hex_num_item)

@settings(verbosity=vb)
@given(octal_number_items())
def test_parses_octal_as_number(oct_num_item):
    form_test(oct_num_item)

@settings(verbosity=vb)
@given(radix_number_items())
def test_parses_radix_as_number(radix_num_item):
    form_test(radix_num_item)

@settings(verbosity=vb)
@given(ratio_items())
def test_parses_ratio_as_number(ratio_item):
    form_test(ratio_item)

@settings(verbosity=vb)
@given(double_items())
def test_parses_double_as_number(double_item):
    form_test(double_item)

@settings(verbosity=vb)
@given(integer_items())
def test_parses_integer_as_number(integer_item):
    form_test(integer_item)

@settings(verbosity=vb)
@given(number_items())
def test_parses_number(number_item):
    form_test(number_item)

## symbols

@settings(verbosity=vb)
@given(unqualified_symbol_items())
def test_parses_unqualified_symbol(unqual_symbol_item):
    form_test(unqual_symbol_item)

@settings(verbosity=vb)
@given(qualified_symbol_items())
def test_parses_qualified_symbol(qual_symbol_item):
    form_test(qual_symbol_item)

## keywords

@settings(verbosity=vb)
@given(unqualified_keyword_items())
def test_parses_unqualified_keyword(unqual_keyword_item):
    form_test(unqual_keyword_item)

@settings(verbosity=vb)
@given(qualified_keyword_items())
def test_parses_qualified_keyword(qual_keyword_item):
    form_test(qual_keyword_item)

@settings(verbosity=vb)
@given(unqualified_auto_resolved_keyword_items())
def test_parses_unqualified_auto_resolved_keyword(unqual_auto_res_keyword_item):
    form_test(unqual_auto_res_keyword_item)

@settings(verbosity=vb)
@given(qualified_auto_resolved_keyword_items())
def test_parses_qualified_auto_resolved_keyword(qual_auto_res_keyword_item):
    form_test(qual_auto_res_keyword_item)

## characters

@settings(verbosity=vb)
@given(any_character_items())
def test_parses_any_character(any_character_item):
    form_test(any_character_item)

@settings(verbosity=vb)
@given(named_character_items())
def test_parses_named_character(named_character_item):
    form_test(named_character_item)

@settings(verbosity=vb)
@given(octal_character_items())
def test_parses_octal_character(octal_character_item):
    form_test(octal_character_item)

@settings(verbosity=vb)
@given(unicode_quad_character_items())
def test_parses_unicode_quad_character(unicode_quad_character_item):
    form_test(unicode_quad_character_item)

@settings(verbosity=vb)
@given(character_items())
def test_parses_character(character_item):
    form_test(character_item)

## strings

@settings(verbosity=vb)
@given(string_items())
def test_parses_string(string_item):
    form_test(string_item)

## lists

@settings(verbosity=vb)
@given(number_list_items())
def test_parses_number_list(num_list_item):
    form_test(num_list_item)

@settings(verbosity=vb)
@given(atom_list_items())
def test_parses_atom_list(atom_list_item):
    form_test(atom_list_item)

## vectors

@settings(verbosity=vb)
@given(number_vector_items())
def test_parses_number_vector(num_vector_item):
    form_test(num_vector_item)

@settings(verbosity=vb)
@given(atom_vector_items())
def test_parses_atom_vector(atom_vector_item):
    form_test(atom_vector_item)

## maps

@settings(verbosity=vb)
@given(number_map_items())
def test_parses_number_map(num_map_item):
    form_test(num_map_item)

@settings(verbosity=vb)
@given(atom_map_items())
def test_parses_atom_map(atom_map_item):
    form_test(atom_map_item)

## metadata

@settings(verbosity=vb)
@given(atom_vector_with_metadata_items())
def test_parses_atom_vector_with_metadata(atom_vector_with_metadata_item):
    form_test(atom_vector_with_metadata_item)

if __name__ == "__main__":
    test_parses_hex_as_number()
    test_parses_octal_as_number()
    test_parses_radix_as_number()
    test_parses_ratio_as_number()
    test_parses_double_as_number()
    test_parses_integer_as_number()
    test_parses_number()
    #
    test_parses_unqualified_symbol()
    test_parses_qualified_symbol()
    #
    test_parses_unqualified_keyword()
    test_parses_qualified_keyword()
    test_parses_unqualified_auto_resolved_keyword()
    test_parses_qualified_auto_resolved_keyword()
    #
    test_parses_any_character()
    test_parses_named_character()
    test_parses_octal_character()
    test_parses_unicode_quad_character()
    test_parses_character()
    #
    test_parses_string()
    #
    test_parses_number_list()
    test_parses_atom_list()
    #
    test_parses_number_vector()
    test_parses_atom_vector()
    #
    test_parses_number_map()
    test_parses_atom_map()
    #
    test_parses_atom_vector_with_metadata()
