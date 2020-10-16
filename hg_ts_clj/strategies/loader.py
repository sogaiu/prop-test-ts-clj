import importlib, os

def get_fns(path):
    if os.path.exists("../verify"):
        module_dict = importlib.import_module("..verify." + path).__dict__
        verify = module_dict["verify"]
        if "verify_with_metadata" in md:
            verify_with_metadata = \
                verify_module.__dict__["verify_with_metadata"]
        else:
            verify_with_metadata = None
    else:
        verify = lambda ctx, item: True
        verify_with_metadata = lambda ctx, item: True
    return verify, verify_with_metadata
