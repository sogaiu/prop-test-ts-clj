"""Hypothesis strategies for tree-sitter-clojure."""

__version__ = '0.0.1'

# XXX: could have assertions for checking has_error?

# XXX: numeric constants being used in strategies are hard-wired -> change?

# XXX: label strings could be factored out (e.g. "map", "number", etc.)

# grammatical pieces
#
# subatomic (1)
#   auto_resolve_marker
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
# compound (17)
#   anon_func
#   deref_form
#   discard_expr
#   eval_form
#   + list
#   + map
#   namespaced_map
#   quote_form
#   read_cond
#   read_cond_splicing
#   set
#   syntax_quote_form
#   tagged_literal
#   unquote_form
#   unquote_splicing_form
#   var_quote_form
#   + vector
#
# compound but not standalone (2)
#   metadata
#   old_metadata
