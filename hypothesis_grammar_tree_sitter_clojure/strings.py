from hypothesis.strategies import composite

from hypothesis_grammar_clojure.strings \
    import string_as_str

@composite
def string_items(draw):
    a_str = draw(string_as_str())
    #
    return (a_str, "string")
