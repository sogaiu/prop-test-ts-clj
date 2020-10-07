"""Hypothesis strategies for tree-sitter-clojure."""

__version__ = '0.0.1'

# XXX: exactly which commit of the grammar that the tests apply to
#      ought to be recorded and tracked.  preferably this could be
#      expressed programmatically as a dependency.  for the moment:
#
#        ab2f869f395a502a8c1b6683cdd68395e62fa96f

# XXX: periodically go through source looking for comments related
#      to unfinished or temporary bits

# XXX: reminder that grammar is in flux so pasted in info in comments
#      needs to be kept up-to-date.

# XXX: verify the limitations of hypothesis_grammar_clojure -- e.g.
#      it currently doesn't handle #! comments.

# XXX: consider how to support old_metadata

# XXX: metadata support still needed for:
#
#        list
#        map
#        set
#        anon_func
#        read_cond
#        read_cond_splicing
#        namespaced_map
#        var_quote_form
#        eval_form
#        tagged_literal
#        syntax_quote_form
#        quote_form
#        unquote_splicing_form
#        unquote_form
#        deref_form

# XXX: the markers of certain forms (e.g. #', @, etc.) are not
#      currently checked.
#
#      it appears that the marker for a node (if any) can be located
#      by finding the first anonymous node.  verify that this
#      assertion is correct.
#
#      currently, markers for collections may not be verified.
#      consider addressing this.
#
#      all things that should have markers checked:
#
#        discard_expr
#        anon_func
#        regex
#        read_cond
#        read_cond_splicing
#        var_quote_form
#        symbolic_value
#        eval_form
#        tagged_literal
#        syntax_quote_form
#        quote_form
#        unquote_splicing_form
#        unquote_form
#        deref_form
#        metadata
#        old_metadata
#
#      unsure:
#
#        keyword - part of value, no anon node
#        string - part of value, no anon node
#        character - part of value, no anon node
#        list
#        map
#        vector
#        namespaced_map
#        set
#        comment
#
#      probably not:
#
#        number
#        nil
#        boolean
#        symbol

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

# XXX: consider placing definitions for verify functions in each
#      form-specific file

# XXX: consider making the "verify" key's value a list of functions
#      which are meant to be used for verification

# XXX: if node.text gets merged in py-tree-sitter and it's usable,
#      consider moving over to that instead of using node_text.
#      n.b. that may require switching from strings to bytes --
#      i.e. use b'hello' instead of 'hello'

# XXX: write up some notes on naming.  could cover terms such as
#      "marker" (meaning things like "#_", "##", etc.)

# XXX: label strings could be factored out (e.g. "map", "number", etc.)
#      perhaps these can be placed in a central look-up table to
#      make changing them later easier (e.g. as a consequence of
#      changing the tree-sitter grammar "grammar symbols")

# XXX: there could also be a lookup table for markers, but this
#      somehow doesn't seem too useful

# XXX: create clojure samples so that s-expression output can be
#      programmatically generated from them when the grammar changes.

# XXX: look into the "deferred" and "data" strategies

# XXX: one piece of tagged_literals.py (tag_items) might have a better
#      home in hypothesis_grammar_clojure.<something>

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
#   old_metadata
