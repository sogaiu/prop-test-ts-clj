from hypothesis.strategies import composite

from .verify import verify_node_as_atom

from hypothesis_grammar_clojure.comments \
    import comment_as_str

# comment: $ =>
#   token(/(;|(#!)).*/),

def build_comment_str(item):
    return item["inputs"]

@composite
def comment_items(draw):
    cmt_str = draw(comment_as_str())
    #
    return {"inputs": cmt_str,
            "label": "comment",
            "to_str": build_comment_str,
            "verify": verify_node_as_atom}
