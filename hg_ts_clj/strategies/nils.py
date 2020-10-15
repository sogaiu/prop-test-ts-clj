from hypothesis.strategies import composite, just

from ..verify.nils import verify

def build_nil_str(item):
    return item["inputs"]

@composite
def nil_items(draw):
    nil_str = draw(just("nil"))
    #
    return {"inputs": nil_str,
            "label": "nil",
            "to_str": build_nil_str,
            "verify": verify}
