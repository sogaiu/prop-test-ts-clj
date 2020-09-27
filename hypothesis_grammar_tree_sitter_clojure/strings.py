from hypothesis.strategies import composite

from hypothesis_grammar_clojure.strings \
    import string_as_str

from .verify import verify_node_as_atom

def build_string_str(item):
    return item["inputs"]

@composite
def string_items(draw):
    a_str_str = draw(string_as_str())
    #
    return {"inputs": a_str_str,
            "label": "string",
            "recipe": build_string_str,
            "verify": verify_node_as_atom}
