from hypothesis.strategies import composite

from .strings import string_items

from .loader import get_fns
import os
verify, _ = get_fns(os.path.basename(__file__))

marker = '#'

def build_regex_str(item):
    str_item = item["inputs"]
    return marker + str_item["to_str"](str_item)

@composite
def regex_items(draw):
    str_item = draw(string_items())
    #
    return {"inputs": str_item,
            "label": "regex",
            "to_str": build_regex_str,
            "verify": verify,
            "marker": marker}
