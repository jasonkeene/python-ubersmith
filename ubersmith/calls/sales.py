"""Sales calls implemented as documented in api docs."""

from ubersmith.calls.base import BaseCall, FlatCall, api_call
from ubersmith.utils import prepend_base

__all__ = []

_METHOD_BASE = "sales"
prepend_base = prepend_base.init(_METHOD_BASE)


# class (BaseCall):
#     method = prepend_base('')


# call functions with proper signatures and docstrings

# @api_call
# def (, request_handler=None):
#     """"""
#     return (request_handler, ).render()
