# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file
from hypothesis import given, note
from hypothesis import settings, HealthCheck, Verbosity

# XXX: clean this up later
from hg_ts_clj.strategies.comments import *
#
from hg_ts_clj.strategies.nils import *
from hg_ts_clj.strategies.booleans import *
from hg_ts_clj.strategies.characters import *
from hg_ts_clj.strategies.keywords import *
from hg_ts_clj.strategies.numbers import *
from hg_ts_clj.strategies.strings import *
from hg_ts_clj.strategies.symbols import *
from hg_ts_clj.strategies.symbolic_values import *
from hg_ts_clj.strategies.regex import *
#
from hg_ts_clj.strategies.atoms import *
#
from hg_ts_clj.strategies.lists import *
from hg_ts_clj.strategies.maps import *
from hg_ts_clj.strategies.namespaced_maps import *
from hg_ts_clj.strategies.sets import *
from hg_ts_clj.strategies.vectors import *
#
from hg_ts_clj.strategies.collections import *
#
from hg_ts_clj.strategies.read_conds import *
from hg_ts_clj.strategies.read_cond_splicings import *
#
from hg_ts_clj.strategies.anon_funcs import *
#
from hg_ts_clj.strategies.deref_forms import *
from hg_ts_clj.strategies.var_quote_forms import *
from hg_ts_clj.strategies.eval_forms import *
from hg_ts_clj.strategies.quote_forms import *
from hg_ts_clj.strategies.syntax_quote_forms import *
from hg_ts_clj.strategies.unquote_forms import *
from hg_ts_clj.strategies.unquote_splicing_forms import *
#
from hg_ts_clj.strategies.tagged_literals import *
#
from hg_ts_clj.strategies.discard_exprs import *
#
from hg_ts_clj.strategies.forms import *

from tree_sitter import Language, Parser

settings.register_profile("basic",
                          parent=None,
                          verbosity=Verbosity.verbose,
                          suppress_health_check=[HealthCheck.too_slow,
                                                 HealthCheck.filter_too_much])
settings.load_profile("basic")

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
    note(f'source: {form_str}\n')
    assert item["verify"](ctx, item), \
        f'verify failed for: {form_str}'

## comments

@given(comment_items())
def test_parses_comment(comment_item):
    form_test(comment_item)

## nils

@given(nil_items())
def test_parses_nil(nil_item):
    form_test(nil_item)

## booleans

@given(boolean_items())
def test_parses_boolean(boolean_item):
    form_test(boolean_item)

## numbers

@given(hex_number_items())
def test_parses_hex_as_number(hex_num_item):
    form_test(hex_num_item)

@given(octal_number_items())
def test_parses_octal_as_number(oct_num_item):
    form_test(oct_num_item)

@given(radix_number_items())
def test_parses_radix_as_number(radix_num_item):
    form_test(radix_num_item)

@given(ratio_items())
def test_parses_ratio_as_number(ratio_item):
    form_test(ratio_item)

@given(double_items())
def test_parses_double_as_number(double_item):
    form_test(double_item)

@given(integer_items())
def test_parses_integer_as_number(integer_item):
    form_test(integer_item)

@given(number_items())
def test_parses_number(number_item):
    form_test(number_item)

## symbols

@given(unqualified_symbol_items())
def test_parses_unqualified_symbol(unqual_symbol_item):
    form_test(unqual_symbol_item)

@given(qualified_symbol_items())
def test_parses_qualified_symbol(qual_symbol_item):
    form_test(qual_symbol_item)

@given(symbol_items())
def test_parses_symbol(symbol_item):
    form_test(symbol_item)

## keywords

@given(unqualified_keyword_items())
def test_parses_unqualified_keyword(unqual_keyword_item):
    form_test(unqual_keyword_item)

@given(qualified_keyword_items())
def test_parses_qualified_keyword(qual_keyword_item):
    form_test(qual_keyword_item)

@given(unqualified_auto_resolved_keyword_items())
def test_parses_unqualified_auto_resolved_keyword(unqual_auto_res_keyword_item):
    form_test(unqual_auto_res_keyword_item)

@given(qualified_auto_resolved_keyword_items())
def test_parses_qualified_auto_resolved_keyword(qual_auto_res_keyword_item):
    form_test(qual_auto_res_keyword_item)

@given(keyword_items())
def test_parses_keyword(keyword_item):
    form_test(keyword_item)

## characters

@given(any_character_items())
def test_parses_any_character(any_character_item):
    form_test(any_character_item)

@given(named_character_items())
def test_parses_named_character(named_character_item):
    form_test(named_character_item)

@given(octal_character_items())
def test_parses_octal_character(octal_character_item):
    form_test(octal_character_item)

@given(unicode_quad_character_items())
def test_parses_unicode_quad_character(unicode_quad_character_item):
    form_test(unicode_quad_character_item)

@given(character_items())
def test_parses_character(character_item):
    form_test(character_item)

## strings

@given(string_items())
def test_parses_string(string_item):
    form_test(string_item)

## symbolic values

@given(symbolic_value_items())
def test_parses_symbolic_value(symbolic_value_item):
    form_test(symbolic_value_item)

## regex

@given(regex_items())
def test_parses_regex(regex_item):
    form_test(regex_item)

## atoms

@given(atom_items())
def test_parses_atom(atom_item):
    form_test(atom_item)

## lists

@given(list_items())
def test_parses_list(list_item):
    form_test(list_item)

## vectors

@given(vector_items())
def test_parses_vector(vector_item):
    form_test(vector_item)

## maps

@given(map_items())
def test_parses_map(map_item):
    form_test(map_item)

## namespaced maps

@given(namespaced_map_items())
def test_parses_namespaced_map(namespaced_map_item):
    form_test(namespaced_map_item)

## sets

@given(set_items())
def test_parses_set(set_item):
    form_test(set_item)

## collections

@given(collection_items())
def test_parses_collection(collection_item):
    form_test(collection_item)

@given(recursive_collection_items())
def test_parses_recursive_collection(rec_coll_item):
    form_test(rec_coll_item)

## reader conditionals

@given(read_cond_items())
def test_parses_reader_conditional(read_cond_item):
    form_test(read_cond_item)

@given(read_cond_splicing_items())
def test_parses_reader_conditional_splicing(read_cond_splicing_item):
    form_test(read_cond_splicing_item)

## anonymous functions

@given(anon_func_items())
def test_parses_anonymous_function(anon_func_item):
    form_test(anon_func_item)

## adorned forms

@given(deref_form_items())
def test_parses_deref_form(deref_form_item):
    form_test(deref_form_item)

@given(var_quote_form_items())
def test_parses_var_quote_form(var_quote_form_item):
    form_test(var_quote_form_item)

@given(eval_form_items())
def test_parses_eval_form(eval_form_item):
    form_test(eval_form_item)

@given(quote_form_items())
def test_parses_quote_form(quote_form_item):
    form_test(quote_form_item)

@given(syntax_quote_form_items())
def test_parses_syntax_quote_form(syntax_quote_form_item):
    form_test(syntax_quote_form_item)

@given(unquote_form_items())
def test_parses_unquote_form(unquote_form_item):
    form_test(unquote_form_item)

@given(unquote_splicing_form_items())
def test_parses_unquote_splicing_form(unquote_splicing_form_item):
    form_test(unquote_splicing_form_item)

## tagged literals

@given(tagged_literal_items())
def test_parses_tagged_literal(tagged_literal_item):
    form_test(tagged_literal_item)

## metadata

@given(symbol_items(metadata="any"))
def test_parses_symbol_with_metadata(symbol_with_metadata_item):
    form_test(symbol_with_metadata_item)

@given(list_items(elements=atom_items(), metadata="any"))
def test_parses_atom_list_with_metadata(atom_list_with_metadata_item):
    form_test(atom_list_with_metadata_item)

@given(map_items(elements=atom_items(), metadata="any"))
def test_parses_atom_map_with_metadata(atom_map_with_metadata_item):
    form_test(atom_map_with_metadata_item)

@given(namespaced_map_items(elements=atom_items(), metadata="any"))
def test_parses_atom_namespaced_map_with_metadata(atom_namespaced_map_with_metadata_item):
    form_test(atom_namespaced_map_with_metadata_item)

@given(set_items(elements=atom_items(), metadata="any"))
def test_parses_atom_set_with_metadata(atom_set_with_metadata_item):
    form_test(atom_set_with_metadata_item)

@given(vector_items(elements=atom_items(), metadata="any"))
def test_parses_atom_vector_with_metadata(atom_vector_with_metadata_item):
    form_test(atom_vector_with_metadata_item)

@given(read_cond_items(metadata="any"))
def test_parses_reader_conditional_with_metadata(read_cond_with_metadata_item):
    form_test(read_cond_with_metadata_item)

@given(read_cond_splicing_items(metadata="any"))
def test_parses_reader_conditional_splicing_with_metadata(read_cond_splicing_with_metadata_item):
    form_test(read_cond_splicing_with_metadata_item)

@given(anon_func_items(metadata="any"))
def test_parses_anonymous_function_with_metadata(anon_func_with_metadata_item):
    form_test(anon_func_with_metadata_item)

@given(deref_form_items(metadata="any"))
def test_parses_deref_form_with_metadata(deref_form_with_metadata_item):
    form_test(deref_form_with_metadata_item)

@given(eval_form_items(metadata="any"))
def test_parses_eval_form_with_metadata(eval_form_with_metadata_item):
    form_test(eval_form_with_metadata_item)

@given(quote_form_items(metadata="any"))
def test_parses_quote_form_with_metadata(quote_form_with_metadata_item):
    form_test(quote_form_with_metadata_item)

@given(syntax_quote_form_items(metadata="any"))
def test_parses_syntax_quote_form_with_metadata(syntax_quote_form_with_metadata_item):
    form_test(syntax_quote_form_with_metadata_item)

@given(unquote_form_items(metadata="any"))
def test_parses_unquote_form_with_metadata(unquote_form_with_metadata_item):
    form_test(unquote_form_with_metadata_item)

@given(unquote_splicing_form_items(metadata="any"))
def test_parses_unquote_splicing_form_with_metadata(unquote_splicing_form_with_metadata_item):
    form_test(unquote_splicing_form_with_metadata_item)

@given(var_quote_form_items(metadata="any"))
def test_parses_var_quote_form_with_metadata(var_quote_form_with_metadata_item):
    form_test(var_quote_form_with_metadata_item)

@given(tagged_literal_items(metadata="any"))
def test_parses_tagged_literal_with_metadata(tagged_literal_with_metadata_item):
    form_test(tagged_literal_with_metadata_item)

## discard expressions

@given(discard_expr_items())
def test_parses_discard_expr(discard_expr_item):
    form_test(discard_expr_item)

## forms

@given(form_items())
def test_parses_form(form_item):
    form_test(form_item)

if __name__ == "__main__":
    test_parses_comment()
    #
    test_parses_nil()
    #
    test_parses_boolean()
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
    test_parses_list()
    test_parses_map()
    test_parses_vector()
    test_parses_set()
    test_parses_namespaced_map()
    #
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
    test_parses_tagged_literal()
    #
    test_parses_symbol_with_metadata()
    test_parses_atom_list_with_metadata()
    test_parses_atom_map_with_metadata()
    test_parses_atom_namespaced_map_with_metadata()
    test_parses_atom_set_with_metadata()
    test_parses_atom_vector_with_metadata()
    test_parses_reader_conditional_with_metadata()
    test_parses_reader_conditional_splicing_with_metadata()
    test_parses_anonymous_function_with_metadata()
    test_parses_deref_form_with_metadata()
    test_parses_eval_form_with_metadata()
    test_parses_quote_form_with_metadata()
    test_parses_syntax_quote_form_with_metadata()
    test_parses_unquote_form_with_metadata()
    test_parses_unquote_splicing_form_with_metadata()
    test_parses_var_quote_form_with_metadata()
    test_parses_tagged_literal_with_metadata()
    #
    test_parses_discard_expr()
    #
    test_parses_form()
    #
