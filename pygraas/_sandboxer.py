from unittest.mock import patch


class RestrictedFunctionError(RuntimeError):
    pass


class RestrictionLayer:
    def __init__(self, vulnerable_functions: list):
        self.patches = []
        self._vulnerable_functions = vulnerable_functions

    def _restrict_function(self, func_path):
        def restricted_func(*args, **kwargs):
            raise RestrictedFunctionError(f"The function '{func_path}' is blocked.")

        patcher = patch(func_path, side_effect=restricted_func)

        self.patches.append(patcher)
        patcher.start()

    def activate(self):
        """Activate the sandbox by patching restricted functions."""
        for function in self._vulnerable_functions:
            self._restrict_function(function)

    def deactivate(self):
        """Deactivate the sandbox and restore original functions."""
        for patcher in self.patches:
            patcher.stop()

        self.patches.clear()
