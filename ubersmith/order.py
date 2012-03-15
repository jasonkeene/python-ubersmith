from ubersmith.calls import generate_generic_calls
from ubersmith.calls.order import (
    GetCall,
    ListCall,
)

__all__ = [
    'get',
    'list',
]


# call functions with proper signatures and docstrings

def get(order_id=None, hash_=None, request_handler=None):
    """Get the details of a specified order."""
    request_data = {}
    if order_id:
        request_data['order_id'] = order_id
    elif hash:
        request_data['hash'] = hash_

    return GetCall(request_data, request_handler).render()


def list(order_step_id=None, order_queue_id=None, brand_id=None,
          step_name=None, min_ts=None, max_ts=None, client_id=None,
          opportunity_id=None, order_by=None, direction=None, offset=None,
          limit=None, request_handler=None):
    """Get a list of orders."""
    request_data = {}
    if order_step_id:
        request_data['order_step_id'] = order_step_id
    if order_queue_id:
        request_data['order_queue_id'] = order_queue_id
    if brand_id:
        request_data['brand_id'] = brand_id
    if step_name:
        request_data['step_name'] = step_name
    if min_ts:
        request_data['min_ts'] = min_ts
    if max_ts:
        request_data['max_ts'] = max_ts
    if client_id:
        request_data['client_id'] = client_id
    if opportunity_id:
        request_data['opportunity_id'] = opportunity_id
    if order_by:
        request_data['order_by'] = order_by
    if direction:
        request_data['direction'] = direction
    if offset:
        request_data['offset'] = offset
    if limit:
        request_data['limit'] = limit

    return ListCall(request_data, request_handler).render()


generate_generic_calls('order', globals())
