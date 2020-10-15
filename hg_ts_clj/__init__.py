"""Hypothesis strategies for tree-sitter-clojure."""

__version__ = '0.0.1'

# XXX: exactly which commit of the grammar that the tests apply to
#      ought to be recorded and tracked.  preferably this could be
#      expressed programmatically as a dependency.  for the moment:
#
#        9df53ae75475e5bdbeb21cd297b8e3160f3b6ed8

# XXX: consider saving generated source strings to feed to a "jailed"
#      clojure process (e.g. in a vm) and log which strings cause
#      parsing issues.

# XXX: try to separate out tree-sitter-specific bits from strategies
#      and figure out how to provide them generically.  e.g.
#      any_character_items currently filters out null bytes, but
#      this limitation is specific to tree-sitter

# XXX: periodically go through source looking for comments related
#      to unfinished or temporary bits

# XXX: write up details on what exactly is being tested and what things
#      are not being tested
#
#        order of nodes
#        existence of nodes
#        node string value
#        node type
#        lack of parse error (has_error)
#          try to visit all nodes to call has_error?
#        whether node was created by ts (i.e. is_missing)
#          try to visit all nodes to call is_missing?
#        markers
#        delimiters
#        distinguishing among nodes even with presence of "separators"
#          determine potential separator locations
#          include locations not between 2 items
#            before first form
#            after last form

# XXX: test execution has following issues:
#
#        non-simple separators complicate perception
#          nicer if start with simple and later use complex separators
#        hypothesis seems to emphasize empty collections (min_size 0)
#          possibly run tests once without min_size 0 and once with 1?
#        only easy to run all tests
#          leads to a lot of commenting / uncommenting
#          fixed order leads to manual reordering
#
#     started using a settings profile.  may be multiple could be
#     made to handle some / all of the above issues.

# XXX: consider making the "verify" key's value a list of functions
#      which are meant to be used for verification

# XXX: write up some notes on naming.  could cover terms such as:
#
#        marker (meaning things like "#_", "##", etc.)
#        metadatee
#        form
#        non-form (separators?)

# XXX: label strings could be factored out (e.g. "map", "number", etc.)
#      perhaps these can be placed in a central look-up table to
#      make changing them later easier (e.g. as a consequence of
#      changing the tree-sitter grammar "grammar symbols")

# XXX: there could also be a lookup table for markers, but this
#      somehow doesn't seem too useful -- a limited form of it ended
#      up being useful for metadata / old_metadata.  not sure if it
#      would be useful for other things.

# XXX: some bits might have a better home in
#      hypothesis_grammar_clojure.<something>, e.g. parts of:
#
#      * nils
#      * regex
#      * symbolic values
#      * tagged_literals
#
#      not sure though

# XXX: verify the limitations of hypothesis_grammar_clojure
#
#        no support for #! comments
#        any_character definition is unverified
#        keywords do not handle non-ascii
#        symbols do not handle non-ascii
#        no real support for collections
#        no escape sequences in strings
#        whitespace is limited to ascii -- is non-ascii whitespace legal?
#        some grammatical constructs missing
#        parameter-tweaking (e.g. number of digits) unexposed

# XXX: if node.text gets merged in py-tree-sitter and it's usable,
#      consider moving over to that instead of using node_text.
#      n.b. that may require switching from strings to bytes --
#      i.e. use b'hello' instead of 'hello'

# grammatical pieces
#
# subatomic (1)
#   + auto_res_marker
#
# atomic (10)
#   + boolean
#   + character
#   + comment
#   + keyword
#   + nil
#   + number
#   + regex
#   + string
#   + symbol
#   + symbolic_value
#
# collection-like (8)
#   + anon_func
#   + list
#   + map
#   + namespaced_map
#   + read_cond
#   + read_cond_splicing
#   + set
#   + vector
#
# adorned form (7)
#   + deref_form
#   + eval_form
#   + quote_form
#   + syntax_quote_form
#   + unquote_form
#   + unquote_splicing_form
#   + var_quote_form
#
# other (2)
#   + discard_expr
#   + tagged_literal
#
# compound but not standalone (2)
#   + metadata
#   + old_metadata
