# clone tree-sitter-clojure into vendor dir and follow setup
# instructions in README for setup before executing this file
from hypothesis import given, note
from hypothesis import settings, HealthCheck, Verbosity


from hypothesis_grammar_clojure import \
    comment_items, \
    nil_items, \
    boolean_items, \
    character_items, \
    keyword_items, \
    number_items, \
    string_items, \
    symbol_items, \
    symbolic_value_items, \
    regex_items, \
    atom_items, \
    list_items, \
    map_items, \
    namespaced_map_items, \
    set_items, \
    vector_items, \
    collection_items, \
    recursive_collection_items, \
    read_cond_items, \
    read_cond_splicing_items, \
    anon_func_items, \
    deref_form_items, \
    var_quote_form_items, \
    eval_form_items, \
    quote_form_items, \
    syntax_quote_form_items, \
    unquote_form_items, \
    unquote_splicing_form_items, \
    tagged_literal_items, \
    discard_expr_items, \
    form_items

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

@given(number_items())
def test_parses_number(number_item):
    form_test(number_item)

## symbols

@given(symbol_items())
def test_parses_symbol(symbol_item):
    form_test(symbol_item)

## keywords

@given(keyword_items())
def test_parses_keyword(keyword_item):
    form_test(keyword_item)

## characters

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
    test_parses_number()
    #
    test_parses_symbol()
    #
    test_parses_keyword()
    #
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
