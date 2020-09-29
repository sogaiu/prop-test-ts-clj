from hypothesis.strategies import composite, one_of

# XXX: change to generic list_items once that exists
from .lists import atom_list_items
# XXX: add reader conditional eventually
from .symbols import symbol_items

from .verify import verify_node_as_adorned

# eval_form: $ =>
#   seq("#=",
#       repeat($._non_form),
#       field('value', choice($.list,
#                             $.read_cond,
#                             // #= ^:a java.lang.String
#                             $.symbol))),

# XXX: there is one separator of interest and that is potentially
#      between #= and the rest of the form.  the default here is
#      no separator.
def build_eval_form_str(item):
    inputs = item["inputs"]
    return "#=" + inputs["to_str"](inputs)

@composite
def eval_form_items(draw):
    legal_item = draw(one_of(atom_list_items(),
                            #read_cond_items(),
                            symbol_items()))
    #
    return {"inputs": legal_item,
            "label": "eval_form",
            "to_str": build_eval_form_str,
            "verify": verify_node_as_adorned}
