from hypothesis.strategies import composite

from hypothesis_grammar_clojure.whitespace \
    import whitespace_as_str

from ..verify.whitespace import verify

def build_whitespace_str(item):
    return item["inputs"]

@composite
def whitespace_items(draw):
    ws_str = draw(whitespace_as_str())
    #
    return {"inputs": ws_str,
            "label": "_whitespace",
            "to_str": build_whitespace_str,
            "verify": verify}
