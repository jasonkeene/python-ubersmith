from ubersmith.api import VALID_METHODS, get_default_request_handler

__all__ = [
    'base',
    'client',
    'device',
    'generate_generic_calls',
    'generic_call',
    'order',
    'sales',
    'support',
    'uber',
]


def generic_call(method, request_handler=None, **kwargs):
    """Generic function to call out to the ubersmith API."""
    handler = request_handler or get_default_request_handler()
    return handler.process_request(method, kwargs)


def generate_generic_calls(prefix, ns):
    for m in VALID_METHODS:
        if m.startswith(u'{}.'.format(prefix)):
            call_name = m.split('.', 1)[1]
            if call_name not in ns:
                ns[call_name] = lambda request_handler=None, **kwargs: \
                                    generic_call(m, request_handler, **kwargs)
                all = ns.get('__all__')
                if all and call_name not in all:
                    all.append(call_name)
