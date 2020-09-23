# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file

from hypothesis import given
from hypothesis import note, settings, Verbosity

# XXX: clean this up later
from hypothesis_grammar_tree_sitter_clojure.characters import *
from hypothesis_grammar_tree_sitter_clojure.keywords import *
from hypothesis_grammar_tree_sitter_clojure.numbers import *
from hypothesis_grammar_tree_sitter_clojure.strings import *
from hypothesis_grammar_tree_sitter_clojure.lists import *
from hypothesis_grammar_tree_sitter_clojure import *

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

## numbers

@settings(verbosity=vb)
@given(hex_number_items())
def test_parses_hex_as_number(hex_num_item):
    the_num, label = hex_num_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(octal_number_items())
def test_parses_octal_as_number(oct_num_item):
    the_num, label = oct_num_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(radix_number_as_str())
def test_parses_radix_as_number(radix_num_str):
    tree = parser.parse(bytes(radix_num_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "number"
    assert radix_num_str == node_text(radix_num_str, child)

@settings(verbosity=vb)
@given(ratio_as_str())
def test_parses_ratio_as_number(ratio_str):
    tree = parser.parse(bytes(ratio_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "number"
    assert ratio_str == node_text(ratio_str, child)

@settings(verbosity=vb)
@given(double_as_str())
def test_parses_double_as_number(dbl_str):
    tree = parser.parse(bytes(dbl_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "number"
    assert dbl_str == node_text(dbl_str, child)

@settings(verbosity=vb)
@given(integer_as_str())
def test_parses_integer_as_number(int_str):
    tree = parser.parse(bytes(int_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "number"
    assert int_str == node_text(int_str, child)

@settings(verbosity=vb)
@given(number_as_str())
def test_parses_number(num_str):
    tree = parser.parse(bytes(num_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "number"
    assert num_str == node_text(num_str, child)

## symbols

@settings(verbosity=vb)
@given(unqualified_symbol_as_str())
def test_parses_unqualified_symbol(symbol_str):
    tree = parser.parse(bytes(symbol_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "symbol"
    assert symbol_str == node_text(symbol_str, child)

@settings(verbosity=vb)
@given(qualified_symbol_as_str())
def test_parses_qualified_symbol(symbol_str):
    tree = parser.parse(bytes(symbol_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "symbol"
    assert symbol_str == node_text(symbol_str, child)

## keywords

@settings(verbosity=vb)
@given(unqualified_keyword_as_str())
def test_parses_unqualified_keyword(keyword_str):
    tree = parser.parse(bytes(keyword_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "keyword"
    assert keyword_str == node_text(keyword_str, child)

@settings(verbosity=vb)
@given(qualified_keyword_as_str())
def test_parses_qualified_keyword(keyword_str):
    tree = parser.parse(bytes(keyword_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "keyword"
    assert keyword_str == node_text(keyword_str, child)

@settings(verbosity=vb)
@given(unqualified_auto_resolved_keyword_as_str())
def test_parses_unqualified_auto_resolved_keyword(keyword_str):
    tree = parser.parse(bytes(keyword_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "keyword"
    assert keyword_str == node_text(keyword_str, child)

@settings(verbosity=vb)
@given(qualified_auto_resolved_keyword_as_str())
def test_parses_qualified_auto_resolved_keyword(keyword_str):
    tree = parser.parse(bytes(keyword_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == "keyword"
    assert keyword_str == node_text(keyword_str, child)

## characters

@settings(verbosity=vb)
@given(any_character_items())
def test_parses_any_character(any_character_item):
    the_chr, label = any_character_item
    tree = parser.parse(bytes(the_chr, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_chr == node_text(the_chr, child)

@settings(verbosity=vb)
@given(named_character_items())
def test_parses_named_character(named_character_item):
    the_chr, label = named_character_item
    tree = parser.parse(bytes(the_chr, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_chr == node_text(the_chr, child)

@settings(verbosity=vb)
@given(octal_character_items())
def test_parses_octal_character(octal_character_item):
    the_chr, label = octal_character_item
    tree = parser.parse(bytes(the_chr, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_chr == node_text(the_chr, child)

@settings(verbosity=vb)
@given(unicode_quad_character_items())
def test_parses_unicode_quad_character(unicode_quad_character_item):
    the_chr, label = unicode_quad_character_item
    tree = parser.parse(bytes(the_chr, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_chr == node_text(the_chr, child)

@settings(verbosity=vb)
@given(character_items())
def test_parses_character(character_item):
    the_chr, label = character_item
    tree = parser.parse(bytes(the_chr, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_chr == node_text(the_chr, child)

## strings

@settings(verbosity=vb)
@given(string_items())
def test_parses_string(string_item):
    the_str, label = string_item
    tree = parser.parse(bytes(the_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_str == node_text(the_str, child)

## lists

@settings(verbosity=vb)
@given(number_list_items())
def test_parses_number_list(num_list_item):
    (list_str, label), num_items = num_list_item
    tree = parser.parse(bytes(list_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    the_list_node = root_node.children[0]
    assert the_list_node.type == label
    cnt = 0
    for child in the_list_node.children:
        if child.is_named:
            child_text = node_text(list_str, child)
            a_num, a_type = num_items[cnt]
            assert child_text == a_num
            assert child.type == a_type
            cnt += 1
    assert len(num_items) == cnt

@settings(verbosity=vb)
@given(atom_list_items())
def test_parses_atom_list(atm_list_item):
    (list_str, label), atm_items = atm_list_item
    tree = parser.parse(bytes(list_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    the_list_node = root_node.children[0]
    assert the_list_node.type == label
    cnt = 0
    for child in the_list_node.children:
        if child.is_named:
            child_text = node_text(list_str, child)
            an_atm, a_type = atm_items[cnt]
            assert child_text == an_atm
            assert child.type == a_type
            cnt += 1
    assert len(atm_items) == cnt

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
