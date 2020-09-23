# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file

from hypothesis import given
from hypothesis import note, settings, Verbosity

# XXX: clean this up later
from hypothesis_grammar_tree_sitter_clojure.characters import *
from hypothesis_grammar_tree_sitter_clojure.keywords import *
from hypothesis_grammar_tree_sitter_clojure.numbers import *
from hypothesis_grammar_tree_sitter_clojure.strings import *
from hypothesis_grammar_tree_sitter_clojure.symbols import *
from hypothesis_grammar_tree_sitter_clojure.vectors import *
from hypothesis_grammar_tree_sitter_clojure.lists import *

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
@given(radix_number_items())
def test_parses_radix_as_number(radix_num_item):
    the_num, label = radix_num_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(ratio_items())
def test_parses_ratio_as_number(ratio_item):
    the_num, label = ratio_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(double_items())
def test_parses_double_as_number(double_item):
    the_num, label = double_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(integer_items())
def test_parses_integer_as_number(integer_item):
    the_num, label = integer_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

@settings(verbosity=vb)
@given(number_items())
def test_parses_number(number_item):
    the_num, label = number_item
    tree = parser.parse(bytes(the_num, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_num == node_text(the_num, child)

## symbols

@settings(verbosity=vb)
@given(unqualified_symbol_items())
def test_parses_unqualified_symbol(unqualified_symbol_item):
    the_sym, label = unqualified_symbol_item
    tree = parser.parse(bytes(the_sym, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_sym == node_text(the_sym, child)

@settings(verbosity=vb)
@given(qualified_symbol_items())
def test_parses_qualified_symbol(qualified_symbol_item):
    the_sym, label = qualified_symbol_item
    tree = parser.parse(bytes(the_sym, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_sym == node_text(the_sym, child)

## keywords

@settings(verbosity=vb)
@given(unqualified_keyword_items())
def test_parses_unqualified_keyword(unqualified_keyword_item):
    the_kwd, label = unqualified_keyword_item
    tree = parser.parse(bytes(the_kwd, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_kwd == node_text(the_kwd, child)

@settings(verbosity=vb)
@given(qualified_keyword_items())
def test_parses_qualified_keyword(qual_keyword_item):
    the_kwd, label = qual_keyword_item
    tree = parser.parse(bytes(the_kwd, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_kwd == node_text(the_kwd, child)

@settings(verbosity=vb)
@given(unqualified_auto_resolved_keyword_items())
def test_parses_unqualified_auto_resolved_keyword(unqual_auto_res_keyword_item):
    the_kwd, label = unqual_auto_res_keyword_item
    tree = parser.parse(bytes(the_kwd, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_kwd == node_text(the_kwd, child)

@settings(verbosity=vb)
@given(qualified_auto_resolved_keyword_items())
def test_parses_qualified_auto_resolved_keyword(qual_auto_res_keyword_item):
    the_kwd, label = qual_auto_res_keyword_item
    tree = parser.parse(bytes(the_kwd, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    child = root_node.children[0]
    assert child.type == label
    assert the_kwd == node_text(the_kwd, child)

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

## vectors

@settings(verbosity=vb)
@given(number_vector_items())
def test_parses_number_vector(num_vector_item):
    (vector_str, label), num_items = num_vector_item
    tree = parser.parse(bytes(vector_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    the_vector_node = root_node.children[0]
    assert the_vector_node.type == label
    cnt = 0
    for child in the_vector_node.children:
        if child.is_named:
            child_text = node_text(vector_str, child)
            a_num, a_type = num_items[cnt]
            assert child_text == a_num
            assert child.type == a_type
            cnt += 1
    assert len(num_items) == cnt

@settings(verbosity=vb)
@given(atom_vector_items())
def test_parses_atom_vector(atm_vector_item):
    (vector_str, label), atm_items = atm_vector_item
    tree = parser.parse(bytes(vector_str, "utf8"))
    root_node = tree.root_node
    assert 1 == len(root_node.children)
    the_vector_node = root_node.children[0]
    assert the_vector_node.type == label
    cnt = 0
    for child in the_vector_node.children:
        if child.is_named:
            child_text = node_text(vector_str, child)
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
    test_parses_number_vector()
    test_parses_atom_vector()
