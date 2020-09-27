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
#
from hypothesis_grammar_tree_sitter_clojure.atoms import *
#
from hypothesis_grammar_tree_sitter_clojure.lists import *
from hypothesis_grammar_tree_sitter_clojure.maps import *
from hypothesis_grammar_tree_sitter_clojure.vectors import *
#
from hypothesis_grammar_tree_sitter_clojure.collections import *
#
from hypothesis_grammar_tree_sitter_clojure.quote_forms import *
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

def form_test(item):
    form_str = item["recipe"](item)
    ctx = {"node": get_lone_node(form_str),
           "source": form_str}
    assert item["verify"](ctx, item)

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

@settings(verbosity=vb)
@given(symbol_items())
def test_parses_symbol(symbol_item):
    form_test(symbol_item)

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

@settings(verbosity=vb)
@given(keyword_items())
def test_parses_keyword(keyword_item):
    form_test(keyword_item)

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

## atoms

@settings(verbosity=vb)
@given(atom_items())
def test_parses_atom(atom_item):
    form_test(atom_item)

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

## collections

@settings(verbosity=vb)
@given(atom_collection_items())
def test_parses_atom_collection(atom_collection_item):
    form_test(atom_collection_item)

## adorned forms

@settings(verbosity=vb)
@given(quote_form_items())
def test_parses_quote_form(quote_form_item):
    form_test(quote_form_item)

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
    test_parses_symbol()
    #
    test_parses_unqualified_keyword()
    test_parses_qualified_keyword()
    test_parses_unqualified_auto_resolved_keyword()
    test_parses_qualified_auto_resolved_keyword()
    test_parses_keyword()
    #
    test_parses_any_character()
    test_parses_named_character()
    test_parses_octal_character()
    test_parses_unicode_quad_character()
    test_parses_character()
    #
    test_parses_string()
    #
    test_parses_atom()
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
    test_parses_atom_collection()
    #
    test_parses_quote_form()
    #
    test_parses_atom_vector_with_metadata()
    #
