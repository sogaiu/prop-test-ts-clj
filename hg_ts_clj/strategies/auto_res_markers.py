from hypothesis.strategies import composite, just

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

def build_auto_res_marker_str(item):
    # this is just "::"
    return item["inputs"]

@composite
def auto_res_marker_items(draw):
    arm_item = draw(just("::"))
    #
    return {"inputs": arm_item,
            "label": "auto_res_marker",
            "to_str": build_auto_res_marker_str,
            "verify": verify}
