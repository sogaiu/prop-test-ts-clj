from hypothesis.strategies import composite, one_of

# XXX: change to generic list_items once that exists
from .lists import atom_list_items
# XXX: add reader conditional eventually
from .symbols import symbol_items

from .verify import verify_node_as_adorned

# XXX: alternative ways of providing separation between elements?
#      obvious way is whitespace, but could also have:
#
#      * line comment that extends to end of line
#      * discard form
#      * combination
#
#      perhaps better to have a strategy for generating such
#      "spacing" or "separation" units
#
#      there is one separator of interest and that is potentially
#      between #= and the rest of the form.  the default here is
#      no separator.
def build_eval_form_str(item):
    inputs = item["inputs"]
    return "#=" + inputs["recipe"](inputs)

@composite
def eval_form_items(draw):
    legal_item = draw(one_of(atom_list_items(),
                            #read_cond_items(),
                            symbol_items()))
    #
    return {"inputs": legal_item,
            "label": "eval_form",
            "recipe": build_eval_form_str,
            "verify": verify_node_as_adorned}
