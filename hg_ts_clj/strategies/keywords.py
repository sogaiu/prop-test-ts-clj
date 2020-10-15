from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.keywords \
    import unqualified_auto_resolved_keyword_as_str, \
           unqualified_keyword_as_str, \
           qualified_auto_resolved_keyword_as_str, \
           qualified_keyword_as_str

from ..verify.keywords import verify

# const KEYWORD =
#       token(choice(// :my-ns/hi
#                    // :a
#                    // :/ is neither invalid nor valid, but repl accepts
#                    seq(":",
#                        choice("/",
#                              KEYWORD_NO_SIGIL)),
#                    // ::my-alias/hi
#                    // ::a
#                    // ::/ is invalid
#                    seq(AUTO_RESOLVE_MARKER,
#                        KEYWORD_NO_SIGIL)));

def build_kwd_str(item):
    return item["inputs"]

@composite
def unqualified_auto_resolved_keyword_items(draw):
    kwd_str = draw(unqualified_auto_resolved_keyword_as_str())
    #
    return {"inputs": kwd_str,
            "label": "keyword",
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def unqualified_keyword_items(draw):
    kwd_str = draw(unqualified_keyword_as_str())
    #
    return {"inputs": kwd_str,
            "label": "keyword",
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def qualified_auto_resolved_keyword_items(draw):
    kwd_str = draw(qualified_auto_resolved_keyword_as_str())
    #
    return {"inputs": kwd_str,
            "label": "keyword",
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def qualified_keyword_items(draw):
    kwd_str = draw(qualified_keyword_as_str())
    #
    return {"inputs": kwd_str,
            "label": "keyword",
            "to_str": build_kwd_str,
            "verify": verify}

@composite
def keyword_items(draw):
    kwd_item = draw(one_of(unqualified_auto_resolved_keyword_items(),
                           unqualified_keyword_items(),
                           qualified_auto_resolved_keyword_items(),
                           qualified_keyword_items()))
    return kwd_item
