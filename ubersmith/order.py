from ubersmith.calls.base import api_call
from ubersmith.calls.order import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions with proper signatures and docstrings

@api_call
def get(order_id=None, hash_=None, request_handler=None):
    """Get the details of a specified order."""
    return GetCall(request_handler, order_id, hash_).render()


@api_call
def list(order_step_id=None, order_queue_id=None, brand_id=None,
          step_name=None, min_ts=None, max_ts=None, client_id=None,
          opportunity_id=None, order_by=None, direction=None, offset=None,
          limit=None, request_handler=None):
    """Get a list of orders."""
    return ListCall(request_handler, order_step_id, order_queue_id, brand_id,
                     step_name, min_ts, max_ts, client_id, opportunity_id,
                     order_by, direction, offset, limit).render()
