from hypothesis import assume
from hypothesis.strategies import composite, lists, sampled_from

from .symbols import symbol_items

from .forms import form_items

from .separators import separator_strings

from .verify import verify_node_as_adorned, \
    make_single_verifier

marker = '#'

# tagged_literal: $ =>
#   seq(repeat($._metadata),
#       "#",
#       // # uuid "00000000-0000-0000-0000-000000000000"
#       // # #_ 1 uuid "00000000-0000-0000-0000-000000000000"
#       // etc.
#       repeat($._non_form),
#       // # ^:a uuid "00000000-0000-0000-0000-000000000000"
#       field('tag', $.symbol),
#       repeat($._non_form),
#       field('value', choice($._form))),

# XXX: could also have stuff before and after delimiters
def build_tagged_literal_str(tagged_literal_item):
    form_item = tagged_literal_item["inputs"]
    form_str = form_item["to_str"](form_item)
    #
    seps = tagged_literal_item["separators"]
    #
    tag_item = tagged_literal_item["tag"]
    tag_str = tag_item["to_str"](tag_item)
    #
    # XXX: consider again later
    #return "#" + seps[0] + tag_str + seps[1] + form_str
    return marker + tag_str + " " + form_str

# XXX: may want to move parts to:
#
#        hypothesis_grammar_clojure.<something>
#
#     at some point
@composite
def tag_items(draw):
    # XXX: symbol with metadata should be possible too...
    #      may need to go over other parts of code to find
    #      similar cases
    tag_item = draw(symbol_items())
    #
    # "# followed immediately by a symbol starting with an alphabetic
    #  character indicates that that symbol is a tag"
    #
    # via: https://github.com/edn-format/edn#tagged-elements
    #
    tag_head = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z",
                "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y", "Z"]
    tag_head_str = draw(sampled_from(tag_head))
    #
    tag_item["inputs"] = tag_head_str + tag_item["inputs"]
    #
    return tag_item

def verify(ctx, item):
    return make_single_verifier("tag")(ctx, item) and \
        verify_node_as_adorned(ctx, item)

@composite
def tagged_literal_items(draw):
    form_item = draw(form_items())
    #
    tag_item = draw(tag_items())
    #
    sep_strs = draw(lists(elements=separator_strings(),
                          min_size=2, max_size=2))
    #
    return {"inputs": form_item,
            "label": "tagged_literal",
            "to_str": build_tagged_literal_str,
            "verify": verify,
            "tag": tag_item,
            "separators": sep_strs,
            "marker": marker}
