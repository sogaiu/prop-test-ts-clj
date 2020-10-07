from hypothesis.strategies import integers
from hypothesis.strategies import composite, lists

from math import floor

from .parameters import coll_max

from .forms import form_items
from .keywords import keyword_items

from .separators import separator_strings

from .verify import verify_node_as_coll

# read_cond_splicing: $ =>
#   // XXX: metadata here doesn't seem to make sense, but the repl
#   //      will accept: [^:x #?@(:clj [[:a]] :cljr [[:b]])]
#   seq(repeat($._metadata),
#       "#?@",
#       repeat($._whitespace),
#       $._bare_list),
#
# _bare_list: $ =>
#   seq("(",
#       repeat(choice(field('value', $._form),
#                     $._non_form)),
#       ")"),

marker = "#?@"

# XXX: could also have stuff before and after delimiters
def build_read_cond_splicing_str(read_cond_splicing_item):
    items = read_cond_splicing_item["inputs"]
    seps = read_cond_splicing_item["separators"]
    read_cond_splicing_elts = []
    for i, s in zip(items, seps):
        read_cond_splicing_elts += i["to_str"](i) + s
    # XXX: there can be whitespace between #?@ and (
    return marker + "" + "(" + "".join(read_cond_splicing_elts) + ")"

@composite
def read_cond_splicing_items(draw):
    n = draw(integers(min_value=0, max_value=floor(coll_max/2)))
    # XXX: may be auto-resolved are not allowed?
    kwd_items = draw(lists(elements=keyword_items(),
                           min_size=0, max_size=n))
    #
    frm_items = draw(lists(elements=form_items(),
                           min_size=0, max_size=n))
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=2*n, max_size=2*n))
    items = [item
             for pair in zip(kwd_items, frm_items)
             for item in pair]
    #
    return {"inputs": items,
            "label": "read_cond_splicing",
            "to_str": build_read_cond_splicing_str,
            "verify": verify_node_as_coll,
            "separators": sep_strs,
            "marker": marker}
