from hypothesis.strategies import composite

from hypothesis_grammar_clojure.whitespace \
    import whitespace_as_str

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_whitespace_str(item):
    return item["inputs"]

@composite
def whitespace_items(draw):
    ws_str = draw(whitespace_as_str())
    #
    return {"inputs": ws_str,
            "label": label,
            "to_str": build_whitespace_str,
            "verify": verify}
