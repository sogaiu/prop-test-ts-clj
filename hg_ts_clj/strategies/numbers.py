from hypothesis.strategies import composite, one_of

from hypothesis_grammar_clojure.numbers \
    import radix_number_as_str, \
           hex_number_as_str, \
           octal_number_as_str, \
           ratio_as_str, \
           double_as_str, \
           integer_as_str

from .loader import verify_fns, label_for
import os
name = os.path.splitext(os.path.basename(__file__))[0]
verify, _ = verify_fns(name)
label = label_for(name)

def build_num_str(item):
    return item["inputs"]

@composite
def hex_number_items(draw):
    num_str = draw(hex_number_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def octal_number_items(draw):
    num_str = draw(octal_number_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def radix_number_items(draw):
    num_str = draw(radix_number_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def ratio_items(draw):
    num_str = draw(ratio_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def double_items(draw):
    num_str = draw(double_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def integer_items(draw):
    num_str = draw(integer_as_str())
    #
    return {"inputs": num_str,
            "label": label,
            "to_str": build_num_str,
            "verify": verify}

@composite
def number_items(draw):
    num_item = draw(one_of(radix_number_items(),
                           hex_number_items(),
                           octal_number_items(),
                           ratio_items(),
                           double_items(),
                           integer_items()))
    return num_item
