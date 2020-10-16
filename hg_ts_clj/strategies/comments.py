from hypothesis.strategies import composite

from hypothesis_grammar_clojure.comments \
    import comment_as_str

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_comment_str(item):
    return item["inputs"]

@composite
def comment_items(draw):
    cmt_str = draw(comment_as_str())
    #
    return {"inputs": cmt_str,
            "label": label,
            "to_str": build_comment_str,
            "verify": verify}
