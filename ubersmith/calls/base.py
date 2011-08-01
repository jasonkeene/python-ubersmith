# the base classes for all other calls go here

import inspect as _inspect

from ubersmith.api import get_default_request_handler as _get_default_handler
from ubersmith.decorator import decorator as _wrap


class _BaseCall(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def render(self):
        raise NotImplementedError(
            "No render method defined for {0}".format(self.__class__))


class _DemoCall(_BaseCall):
    def __init__(self, request_handler, object_id):
        super(_DemoCall, self).__init__(request_handler)
        self.object_id = object_id

    def render(self):
        return "Render _DemoCall object_id: {0}".format(self.object_id)


def _signature_position(func, arg_name):
    """Look at func's signature and return the position of arg_name."""
    return _inspect.getargspec(func).args.index(arg_name)


def _api_call_wrapper(call_func, *args):
    """If caller did not provide a request_handler, use the default."""
    index = _signature_position(call_func, 'request_handler')
    args = list(args)  # convert tuple to a mutable type
    args[index] = args[index] or _get_default_handler()

    return call_func(*args)


def _api_call_definition_check(call_func):
    """Check that call_func accepts a request_handler argument."""
    try:
        _signature_position(call_func, 'request_handler')
    except ValueError:
        raise Exception("API call '{0}' defined without a request_handler " \
                                      "argument.".format(call_func.func_name))


def _api_call(call_func):
    """Decorate API call function."""
    _api_call_definition_check(call_func)

    return _wrap(_api_call_wrapper, call_func)


# convenience functions w/ proper signatures and documentation

@_api_call
def demo_call(object_id, request_handler=None):
    """Awesome doc string!"""
    return _DemoCall(request_handler, object_id).render()


@_api_call
def demo_call2(object_id, client_id, request_handler=None):
    """Awesome doc string!2"""
    return _DemoCall(request_handler, object_id, client_id).render()


@_api_call
def demo_call3(client_id, request_handler=None):
    """Awesome doc string!3"""
    return _DemoCall(request_handler, client_id).render()


if __name__ == '__main__':
    # pass
    help(demo_call3)
    from ubersmith.api import RequestHandler, set_default_request_handler
    set_default_request_handler(RequestHandler())
    print demo_call(765)
    print demo_call(126)
    print demo_call(56854, RequestHandler())
    print demo_call(467, request_handler=RequestHandler())
