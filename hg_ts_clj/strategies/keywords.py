from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.keywords \
    import unqualified_auto_resolved_keyword_as_str, \
           unqualified_keyword_as_str, \
           qualified_auto_resolved_keyword_as_str, \
           qualified_keyword_as_str

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

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
