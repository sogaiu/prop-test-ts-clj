from hypothesis.strategies import composite

from .strings import string_items

from .verify import verify_node_type_text_and_no_error, \
    verify_node_marker

# regex: $ =>
#   seq("#",
#       STRING),

marker = '#'

def build_regex_str(item):
    str_item = item["inputs"]
    return marker + str_item["to_str"](str_item)

def verify(ctx, item):
    return verify_node_type_text_and_no_error(ctx, item) and \
        verify_node_marker(ctx, item)

# XXX: may want to move parts to:
#
#        hypothesis_grammar_clojure.<something>
#
#     at some point
@composite
def regex_items(draw):
    str_item = draw(string_items())
    #
    return {"inputs": str_item,
            "label": "regex",
            "to_str": build_regex_str,
            "verify": verify,
            "marker": marker}
