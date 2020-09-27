from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.keywords \
    import unqualified_auto_resolved_keyword_as_str, \
           unqualified_keyword_as_str, \
           qualified_auto_resolved_keyword_as_str, \
           qualified_keyword_as_str

from .verify import verify_node_as_atom

def build_kwd_str(item):
    return item["inputs"]

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "keyword", should the following be labeled
#      "unqualified_auto_resolved_keyword"?
@composite
def unqualified_auto_resolved_keyword_items(draw):
    a_kwd_str = draw(unqualified_auto_resolved_keyword_as_str())
    #
    return {"inputs": a_kwd_str,
            "label": "keyword",
            "recipe": build_kwd_str,
            "verify": verify_node_as_atom}

@composite
def unqualified_keyword_items(draw):
    a_kwd_str = draw(unqualified_keyword_as_str())
    #
    return {"inputs": a_kwd_str,
            "label": "keyword",
            "recipe": build_kwd_str,
            "verify": verify_node_as_atom}

@composite
def qualified_auto_resolved_keyword_items(draw):
    a_kwd_str = draw(qualified_auto_resolved_keyword_as_str())
    #
    return {"inputs": a_kwd_str,
            "label": "keyword",
            "recipe": build_kwd_str,
            "verify": verify_node_as_atom}

@composite
def qualified_keyword_items(draw):
    a_kwd_str = draw(qualified_keyword_as_str())
    #
    return {"inputs": a_kwd_str,
            "label": "keyword",
            "recipe": build_kwd_str,
            "verify": verify_node_as_atom}

@composite
def keyword_items(draw):
    a_kwd_item = draw(one_of(unqualified_auto_resolved_keyword_items(),
                             unqualified_keyword_items(),
                             qualified_auto_resolved_keyword_items(),
                             qualified_keyword_items()))
    return a_kwd_item
