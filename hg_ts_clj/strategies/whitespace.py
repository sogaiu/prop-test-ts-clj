from hypothesis.strategies import composite

from hypothesis_grammar_clojure.whitespace \
    import whitespace_as_str

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

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
