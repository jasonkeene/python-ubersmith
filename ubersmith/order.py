"""Order call functions.

These are light weight call functions that basically just wrap call classes
under ubersmith.calls.  If a call function doesn't exist it will be generated
by generate_generic_calls which searches for a call class and if one isn't
found one is created using ubersmith.calls.BaseCall.

"""

from ubersmith.calls import generate_generic_calls

__all__ = []


generate_generic_calls(__name__.split('.')[-1], globals())
