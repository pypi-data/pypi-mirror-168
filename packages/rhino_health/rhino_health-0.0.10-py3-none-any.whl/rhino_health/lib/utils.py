import logging
import sys


def url_for(base_url, endpoint):
    # Urljoin doesn't actually work correctly
    return f"{base_url.strip().rstrip('/')}/{endpoint.strip().lstrip('/')}"


class RhinoSDKException(Exception):
    """
    @autoapi False
    Use this in order to conditionally suppress stack traces
    """

    def __init__(self, original_exception):
        if isinstance(original_exception, str):
            self.original_class = self.__class__
            self.original_class_name = "RhinoSDKException"
        else:
            self.original_class = original_exception.__class__
            self.original_class_name = self.original_class.__name__
        super(RhinoSDKException, self).__init__(original_exception)

    @property
    def __name__(self):
        return self.original_class_name


def setup_traceback(old_exception_handler, show_traceback):
    def rhino_exeception_handler(error_type, error_value, traceback):
        is_rhino_exception = error_type == RhinoSDKException
        original_error_type = error_value.original_class if is_rhino_exception else error_type
        if not show_traceback and is_rhino_exception:
            print(": ".join([str(error_value.__name__), str(error_value)]))
        else:
            old_exception_handler(original_error_type, error_value, traceback)

    if hasattr(__builtins__, "__IPYTHON__") or "ipykernel" in sys.modules:
        logging.debug("Setting up IPython override")
        ipython = (
            get_ipython()
        )  # This exists in globals if we are in ipython, don't worry unresolved

        def rhino_ipython_handler(shell, error_type, error_value, tb, **kwargs):
            if not show_traceback:
                print(": ".join([str(error_value.__name__), str(error_value)]))
            else:
                shell.showtraceback((error_value.original_class, error_value, tb))

        # this registers a custom exception handler for the whole current notebook
        ipython.set_custom_exc((RhinoSDKException,), rhino_ipython_handler)
    else:
        logging.debug("Setting up default python override")
        sys.excepthook = rhino_exeception_handler


def rhino_error_wrapper(func):
    """
    Add this decorator to the top level call to ensure the traceback suppression works
    """

    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, RhinoSDKException):
                raise
            raise RhinoSDKException(e) from e

    return wrapper_func
