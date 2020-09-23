from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.keywords \
    import unqualified_auto_resolved_keyword_as_str, \
           unqualified_keyword_as_str, \
           qualified_auto_resolved_keyword_as_str, \
           qualified_keyword_as_str

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "keyword", should the following be labeled
#      "unqualified_auto_resolved_keyword"?
@composite
def unqualified_auto_resolved_keyword_items(draw):
    a_kwd = draw(unqualified_auto_resolved_keyword_as_str())
    #
    return (a_kwd, "keyword")

@composite
def unqualified_keyword_items(draw):
    a_kwd = draw(unqualified_keyword_as_str())
    #
    return (a_kwd, "keyword")

@composite
def qualified_auto_resolved_keyword_items(draw):
    a_kwd = draw(qualified_auto_resolved_keyword_as_str())
    #
    return (a_kwd, "keyword")

@composite
def qualified_keyword_items(draw):
    a_kwd = draw(qualified_keyword_as_str())
    #
    return (a_kwd, "keyword")

@composite
def keyword_items(draw):
    a_kwd, label = draw(one_of(unqualified_auto_resolved_keyword_items(),
                               unqualified_keyword_items(),
                               qualified_auto_resolved_keyword_items(),
                               qualified_keyword_items()))
    # XXX: whether label should be passed through...
    return (a_kwd, "keyword")
