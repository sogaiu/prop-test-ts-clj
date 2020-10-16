from hypothesis.strategies import composite, just, one_of

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

def build_boolean_str(item):
    return item["inputs"]

@composite
def boolean_items(draw):
    bool_str = draw(one_of(just("false"), just("true")))
    #
    return {"inputs": bool_str,
            "label": "boolean",
            "to_str": build_boolean_str,
            "verify": verify}
