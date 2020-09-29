from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists, one_of, sampled_from

from .comments import comment_items
from .discard_exprs import discard_expr_items

# _non_form: $ =>
#   choice($._whitespace,
#          $.comment,
#          $.discard_expr),

# XXX: move to hypothesis_grammar_clojure.whitespace?
@composite
def whitespace_strings(draw):
    allowed = ["\f", "\n", "\r", "\t", ",", " "]
    #
    n = draw(integers(min_value=1, max_value=19))
    #
    ws_chars = \
        draw(lists(elements=sampled_from(allowed),
                   min_size=n, max_size=n))
    ws_str = "".join(ws_chars)
    #
    return ws_str

# newline is appended so result can be used as a separator
@composite
def comment_and_nl_strings(draw):
    cmt_item = draw(comment_items())
    #
    return cmt_item["to_str"](cmt_item) + "\n"

# space is appended so result can be used safely as a separator
@composite
def discard_expr_and_ws_strings(draw):
    de_item = draw(discard_expr_items())
    # XXX: prepend single space until the following is fixed?
    #
    #        https://github.com/sogaiu/tree-sitter-clojure/issues/7
    #
    #return de_item["to_str"](de_item) + " "
    return " " + de_item["to_str"](de_item) + " "

@composite
def separator_strings(draw):
    n = draw(integers(min_value=1, max_value=10))
    #
    seps = \
        draw(lists(elements=one_of(whitespace_strings(),
                                   comment_and_nl_strings(),
                                   discard_expr_and_ws_strings()),
                   min_size=n, max_size=n))
    sep_str = "".join(seps)
    #
    return sep_str
