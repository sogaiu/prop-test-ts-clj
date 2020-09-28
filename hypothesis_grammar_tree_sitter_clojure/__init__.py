"""Hypothesis strategies for tree-sitter-clojure."""

__version__ = '0.0.1'

# XXX: could have assertions for checking has_error?

# XXX: may be py-tree-sitter doesn't provide access to is_missing?

# XXX: numeric constants being used in strategies are hard-wired -> change?

# XXX: label strings could be factored out (e.g. "map", "number", etc.)

# XXX: whether to test a variety of "separators" -- e.g. instead of just
#      a single space:
#
#      * different types and amounts of whitespace,
#      * discard expression
#      * line comment (+ newline, if that's not considered part of comment)

# grammatical pieces
#
# subatomic (1)
#   + auto_res_marker
#
# atomic (10)
#   boolean
#   + character
#   comment
#   + keyword
#   nil
#   + number
#   regex
#   + string
#   + symbol
#   symbolic_value
#
# collection-like (8)
#   anon_func
#   + list
#   + map
#   + namespaced_map
#   read_cond
#   read_cond_splicing
#   set
#   + vector
#
# adorned form (7)
#   + deref_form
#   + eval_form
#   + quote_form
#   syntax_quote_form
#   unquote_form
#   unquote_splicing_form
#   var_quote_form
#
# other (2)
#   discard_expr
#   tagged_literal
#
# compound but not standalone (2)
#   metadata
#   old_metadata
