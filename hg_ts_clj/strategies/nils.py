from hypothesis.strategies import composite, just

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

def build_nil_str(item):
    return item["inputs"]

@composite
def nil_items(draw):
    nil_str = draw(just("nil"))
    #
    return {"inputs": nil_str,
            "label": "nil",
            "to_str": build_nil_str,
            "verify": verify}
