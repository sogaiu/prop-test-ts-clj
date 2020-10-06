"""Hypothesis strategies for tree-sitter-clojure."""

__version__ = '0.0.1'

# XXX: exactly which commit of the grammar that the tests apply to
#      ought to be recorded and tracked.  preferably this could be
#      expressed programmatically as a dependency.  for the moment:
#
#        569cdd8025415077472ef0ba50f8b733f9f1d989

# XXX: reminder that grammar is in flux so pasted in info in comments
#      needs to be kept up-to-date.

# XXX: create clojure samples so that s-expression output can be
#      programmatically generated from them when the grammar changes.

# XXX: the leading portions of certain forms (e.g. #', @, etc.) are
#      not currently checked.  possibly this is a sequence of characters
#      that come after metadata (if there is any metadata).
#
#      things that have leading sequences of characters that don't
#      have leading optional metadata include:
#
#        discard_expr
#        regex
#        symbolic_value
#        eval_form
#
#      in the case of metadata (and old_metadata), check ^ and #^

# XXX: min_size 0 seems worth testing sometimes, but may be it
#      makes sense to have 2 runs of tests, one with min_size 0
#      and another with min_size 1

# XXX: forms.py needs to be filled out.

# XXX: if node.text gets merged in py-tree-sitter and it's usable,
#      consider moving over to that instead of using node_text.
#      n.b. that may require switching from strings to bytes --
#      i.e. use b'hello' instead of 'hello'

# XXX: figure out where else has_error could be applied when
#      verifying nodes

# XXX: py-tree-sitter now has is_missing, so could verify that
#      resulting nodes are not "is_missing"

# XXX: label strings could be factored out (e.g. "map", "number", etc.)
#      perhaps these can be placed in a central look-up table to
#      make changing them later easier (e.g. as a consequence of
#      changing the tree-sitter grammar "grammar symbols")

# XXX: make separator-related bits more tweakable.  start testing with
#      single whitespace and only after things working, make more fancy.

# XXX: find places where separators strategies can / should be applied.
#
#      this may lead to changes in the various verify_* functions
#      as "comment" and "discard_expr" nodes will start showing up.

# XXX: related to separators is the idea of leading or trailing "space"
#      basically the same sorts of things as for separators can go before
#      or after things...need to track down possible locations

# XXX: look into the "deferred" and "data" strategies

# XXX: split prop-test-ts-clj.py into pieces to make running individual /
#      sets of tests easier?  currently a lot of commenting / uncommenting
#      takes place

# grammatical pieces
#
# subatomic (1)
#   + auto_res_marker
#
# atomic (10)
#   boolean
#   + character
#   + comment
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
#   + read_cond
#   read_cond_splicing
#   + set
#   + vector
#
# adorned form (7)
#   + deref_form
#   + eval_form
#   + quote_form
#   syntax_quote_form
#   unquote_form
#   unquote_splicing_form
#   + var_quote_form
#
# other (2)
#   + discard_expr
#   + tagged_literal
#
# compound but not standalone (2)
#   + metadata
#   old_metadata
