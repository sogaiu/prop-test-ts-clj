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

# XXX: periodically go through source looking for comments related
#      to unfinished or temporary bits

# XXX: reminder that grammar is in flux so pasted in info in comments
#      needs to be kept up-to-date.

# XXX: write up details on what exactly is being tested and what things
#      are not being tested
#
#        order of nodes
#        existence of nodes
#        node string value
#        node type
#        lack of parse error
#        whether node was created by ts (i.e. is_missing)
#        markers
#        delimiters
#        distinguishing among nodes even with presence of "separators"

# XXX: find places where separators strategies can / should be applied.
#
#      this may lead to changes in the various verify_* functions
#      as "comment" and "discard_expr" nodes will start showing up.

# XXX: related to separators is the idea of leading or trailing "space"
#      basically the same sorts of things as for separators can go before
#      or after things...need to track down possible locations

# XXX: figure out where else has_error could be applied when
#      verifying nodes

# XXX: py-tree-sitter now has is_missing, so could verify that
#      resulting nodes are not "is_missing"

# XXX: make separator-related bits more tweakable.  start testing with
#      single whitespace and only after things working, make more fancy.

# XXX: min_size 0 seems worth testing sometimes, but may be it
#      makes sense to have 2 runs of tests, one with min_size 0
#      and another with min_size 1

# XXX: split prop-test-ts-clj.py into pieces to make running individual /
#      sets of tests easier?  currently a lot of commenting / uncommenting
#      takes place

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

# XXX: create clojure samples so that s-expression output can be
#      programmatically generated from them when the grammar changes.

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

# XXX: look into the "deferred" and "data" strategies

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
