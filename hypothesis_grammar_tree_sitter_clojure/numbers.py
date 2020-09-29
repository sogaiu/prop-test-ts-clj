from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.numbers \
    import radix_number_as_str, \
           hex_number_as_str, \
           octal_number_as_str, \
           ratio_as_str, \
           double_as_str, \
           integer_as_str

from .verify import verify_node_as_atom

# const NUMBER =
#       token(seq(optional(/[+-]/),
#                 choice(HEX_NUMBER,
#                        OCTAL_NUMBER,
#                        RADIX_NUMBER,
#                        RATIO,
#                        DOUBLE,
#                        INTEGER)));

def build_num_str(item):
    return item["inputs"]

# XXX: should these specialized characters have specialized labels?
#      e.g. instead of "number", should the following be labeled
#      "hex_number"?
@composite
def hex_number_items(draw):
    a_num_str = draw(hex_number_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def octal_number_items(draw):
    a_num_str = draw(octal_number_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def radix_number_items(draw):
    a_num_str = draw(radix_number_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def ratio_items(draw):
    a_num_str = draw(ratio_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def double_items(draw):
    a_num_str = draw(double_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def integer_items(draw):
    a_num_str = draw(integer_as_str())
    #
    return {"inputs": a_num_str,
            "label": "number",
            "recipe": build_num_str,
            "verify": verify_node_as_atom}

@composite
def number_items(draw):
    a_num_item = draw(one_of(radix_number_items(),
                             hex_number_items(),
                             octal_number_items(),
                             ratio_items(),
                             double_items(),
                             integer_items()))
    return a_num_item
