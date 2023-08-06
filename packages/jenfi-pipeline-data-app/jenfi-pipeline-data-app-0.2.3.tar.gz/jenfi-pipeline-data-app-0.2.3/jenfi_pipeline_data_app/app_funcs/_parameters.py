import sys

# This is built specifically to handle loading test variables for papermill.
# EXTREMELY brittle.
def load_test_parameters(self, params_dict):
    mod = sys.modules["__main__"]

    for var_name, var_val in params_dict.items():
        try:
            # If this is defined by papermill or anyone else, we don't want to set it.
            eval(f"mod.{var_name}")
        except (NameError, AttributeError):
            # Papermill nor anyone else defined this variable, let's set it ourselves!
            setattr(mod, var_name, var_val)

def get_parameter(self, var_name):
    mod = sys.modules["__main__"]

    return eval(f"mod.{var_name}")