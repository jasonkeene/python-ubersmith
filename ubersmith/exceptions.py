"""Exceptions for ubersmith library."""

__all__ = [
    'UbersmithError',
    'RequestError',
    'ValidationError',
    'ResponseError',
    'UpdatingTokenResponse',
    'MaintenanceResponse',
]


class UbersmithError(Exception):
    msg = "An error occured with the Ubersmith API."

    def __init__(self, msg=None):
        super(UbersmithError, self).__init__()
        if msg is not None:
            self.msg = msg

    def __str__(self):
        return self.msg


class RequestError(UbersmithError):
    msg = "An error occured with the request to the Ubersmith API."


class ValidationError(RequestError):
    msg = "The request data was invalid for the Ubersmith request."


class ResponseError(UbersmithError):
    """Exception for Ubersmith API Response.

        msg: optional message to pass along w/ stacktrace
        response: decoded json response w/ error info

    """
    msg = "An error occured in the response from the Ubersmith API."

    def __init__(self, msg=None, response=None):
        super(ResponseError, self).__init__(msg)
        if response is not None:
            self.response = response
            self.error_code = response.get('error_code')
            self.error_message = response.get('error_message')
            self.msg = '{0.msg} {0.error_code} {0.error_message}'.format(self)


class UpdatingTokenResponse(ResponseError):
    msg = "Ubersmith is updating token."


class MaintenanceResponse(ResponseError):
    msg = "Ubersmith is currently undergoing maintenance."
