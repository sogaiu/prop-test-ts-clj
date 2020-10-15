from hypothesis.strategies import composite

from hypothesis_grammar_clojure.strings \
    import string_as_str

from ..verify.strings import verify

# const STRING =
#       token(seq('"',
#                 repeat(/[^"\\]/),
#                 repeat(seq("\\",
#                            /./,
#                            repeat(/[^"\\]/))),
#                 '"'));

def build_string_str(item):
    return item["inputs"]

@composite
def string_items(draw):
    str_str = draw(string_as_str())
    #
    return {"inputs": str_str,
            "label": "string",
            "to_str": build_string_str,
            "verify": verify}
