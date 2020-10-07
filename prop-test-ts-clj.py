# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file
from hypothesis import given
from hypothesis import settings, HealthCheck, Verbosity

# XXX: clean this up later
from hypothesis_grammar_tree_sitter_clojure.comments import *
#
from hypothesis_grammar_tree_sitter_clojure.characters import *
from hypothesis_grammar_tree_sitter_clojure.keywords import *
from hypothesis_grammar_tree_sitter_clojure.numbers import *
from hypothesis_grammar_tree_sitter_clojure.strings import *
from hypothesis_grammar_tree_sitter_clojure.symbols import *
from hypothesis_grammar_tree_sitter_clojure.symbolic_values import *
from hypothesis_grammar_tree_sitter_clojure.regex import *
#
from hypothesis_grammar_tree_sitter_clojure.atoms import *
#
from hypothesis_grammar_tree_sitter_clojure.lists import *
from hypothesis_grammar_tree_sitter_clojure.maps import *
from hypothesis_grammar_tree_sitter_clojure.namespaced_maps import *
from hypothesis_grammar_tree_sitter_clojure.sets import *
from hypothesis_grammar_tree_sitter_clojure.vectors import *
#
from hypothesis_grammar_tree_sitter_clojure.collections import *
#
from hypothesis_grammar_tree_sitter_clojure.read_conds import *
from hypothesis_grammar_tree_sitter_clojure.read_cond_splicings import *
#
from hypothesis_grammar_tree_sitter_clojure.anon_funcs import *
#
from hypothesis_grammar_tree_sitter_clojure.deref_forms import *
from hypothesis_grammar_tree_sitter_clojure.var_quote_forms import *
from hypothesis_grammar_tree_sitter_clojure.eval_forms import *
from hypothesis_grammar_tree_sitter_clojure.quote_forms import *
from hypothesis_grammar_tree_sitter_clojure.syntax_quote_forms import *
from hypothesis_grammar_tree_sitter_clojure.unquote_forms import *
from hypothesis_grammar_tree_sitter_clojure.unquote_splicing_forms import *
#
from hypothesis_grammar_tree_sitter_clojure.tagged_literals import *
#
from hypothesis_grammar_tree_sitter_clojure.metadata import *
#
from hypothesis_grammar_tree_sitter_clojure.discard_exprs import *

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
    assert 1 == n_children, \
        f'expected 1 child, found: {n_children} for: {form_str}'
    return children[0]

def form_test(item):
    form_str = item["to_str"](item)
    ctx = {"node": get_lone_node(form_str),
           "source": form_str}
    assert item["verify"](ctx, item), \
        f'verify failed for: {form_str}'

## comments

@settings(verbosity=vb)
@given(comment_items())
def test_parses_comment(comment_item):
    form_test(comment_item)

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

## symbolic values

@settings(verbosity=vb)
@given(symbolic_value_items())
def test_parses_symbolic_value(symbolic_value_item):
    form_test(symbolic_value_item)

## regex

@settings(verbosity=vb)
@given(regex_items())
def test_parses_regex(regex_item):
    form_test(regex_item)

## atoms

@settings(verbosity=vb)
@given(atom_items())
def test_parses_atom(atom_item):
    form_test(atom_item)

## lists

#@settings(verbosity=vb, suppress_health_check=HealthCheck.all())

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(number_list_items())
def test_parses_number_list(num_list_item):
    form_test(num_list_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_list_items())
def test_parses_atom_list(atom_list_item):
    form_test(atom_list_item)

## vectors

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(number_vector_items())
def test_parses_number_vector(num_vector_item):
    form_test(num_vector_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_vector_items())
def test_parses_atom_vector(atom_vector_item):
    form_test(atom_vector_item)

## maps

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(number_map_items())
def test_parses_number_map(num_map_item):
    form_test(num_map_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_map_items())
def test_parses_atom_map(atom_map_item):
    form_test(atom_map_item)

## namespaced maps

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(number_namespaced_map_items())
def test_parses_number_namespaced_map(num_namespaced_map_item):
    form_test(num_namespaced_map_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_namespaced_map_items())
def test_parses_atom_namespaced_map(atom_namespaced_map_item):
    form_test(atom_namespaced_map_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(number_set_items())
def test_parses_number_set(num_set_item):
    form_test(num_set_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_set_items())
def test_parses_atom_set(atom_set_item):
    form_test(atom_set_item)

## collections

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_collection_items())
def test_parses_atom_collection(atom_collection_item):
    form_test(atom_collection_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(recursive_collection_items())
def test_parses_recursive_collection(rec_coll_item):
    form_test(rec_coll_item)

## reader conditionals

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(read_cond_items())
def test_parses_reader_conditional(read_cond_item):
    form_test(read_cond_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(read_cond_splicing_items())
def test_parses_reader_conditional_splicing(read_cond_splicing_item):
    form_test(read_cond_splicing_item)

## anonymous functions

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(anon_func_items())
def test_parses_anonymous_function(anon_func_item):
    form_test(anon_func_item)

## adorned forms

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(deref_form_items())
def test_parses_deref_form(deref_form_item):
    form_test(deref_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(var_quote_form_items())
def test_parses_var_quote_form(var_quote_form_item):
    form_test(var_quote_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(eval_form_items())
def test_parses_eval_form(eval_form_item):
    form_test(eval_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(quote_form_items())
def test_parses_quote_form(quote_form_item):
    form_test(quote_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(syntax_quote_form_items())
def test_parses_syntax_quote_form(syntax_quote_form_item):
    form_test(syntax_quote_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(unquote_form_items())
def test_parses_unquote_form(unquote_form_item):
    form_test(unquote_form_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow])
@given(unquote_splicing_form_items())
def test_parses_unquote_splicing_form(unquote_splicing_form_item):
    form_test(unquote_splicing_form_item)

## metadata

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(symbol_with_metadata_items())
def test_parses_symbol_with_metadata(symbol_with_metadata_item):
    form_test(symbol_with_metadata_item)

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(atom_vector_with_metadata_items())
def test_parses_atom_vector_with_metadata(atom_vector_with_metadata_item):
    form_test(atom_vector_with_metadata_item)

## tagged literals

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(tagged_literal_items())
def test_parses_tagged_literal(tagged_literal_item):
    form_test(tagged_literal_item)

## discard expressions

@settings(verbosity=vb, suppress_health_check=[HealthCheck.too_slow,
                                               HealthCheck.filter_too_much])
@given(discard_expr_items())
def test_parses_discard_expr(discard_expr_item):
    form_test(discard_expr_item)

if __name__ == "__main__":
    test_parses_comment()
    #
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
    test_parses_symbolic_value()
    #
    test_parses_regex()
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
    test_parses_number_namespaced_map()
    test_parses_atom_namespaced_map()
    #
    test_parses_number_set()
    test_parses_atom_set()
    #
    test_parses_atom_collection()
    test_parses_recursive_collection()
    #
    test_parses_reader_conditional()
    test_parses_reader_conditional_splicing()
    #
    test_parses_anonymous_function()
    #
    test_parses_deref_form()
    test_parses_var_quote_form()
    test_parses_eval_form()
    test_parses_quote_form()
    test_parses_syntax_quote_form()
    test_parses_unquote_form()
    test_parses_unquote_splicing_form()
    #
    test_parses_symbol_with_metadata()
    test_parses_atom_vector_with_metadata()
    #
    test_parses_tagged_literal()
    #
    test_parses_discard_expr()
    #
