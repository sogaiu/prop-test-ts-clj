from hypothesis.strategies import composite, one_of

# XXX: a lot more to add...
from .atoms import atom_items
from .collections import atom_collection_items

# _form: $ =>
#   choice($.list,
#          $.map,
#          $.vector,
#          // literals
#          $.number,
#          $.keyword,
#          $.string,
#          $.character,
#          $.nil,
#          $.boolean,
#          $.symbol,
#          // dispatch reader macros
#          $.set,
#          $.anon_func,
#          $.regex,
#          $.read_cond,
#          $.read_cond_splicing,
#          $.namespaced_map,
#          $.var_quote_form,
#          $.symbolic_value,
#          $.eval_form,
#          $.tagged_literal,
#          // other reader macros
#          $.syntax_quote_form,
#          $.quote_form,
#          $.unquote_splicing_form,
#          $.unquote_form,
#          $.deref_form),

@composite
def form_items(draw):
    form_item = draw(one_of(atom_items(),
                            atom_collection_items(),
                            # XXX: more to add...
                            ))
    #
    return form_item
