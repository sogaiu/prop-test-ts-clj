from hypothesis.strategies import composite

from hypothesis_grammar_clojure.strings \
    import string_as_str

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_string_str(item):
    return item["inputs"]

@composite
def string_items(draw):
    str_str = draw(string_as_str())
    #
    return {"inputs": str_str,
            "label": label,
            "to_str": build_string_str,
            "verify": verify}
