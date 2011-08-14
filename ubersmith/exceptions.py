# exceptions

__all__ = [
    'BaseError',
    'RequestError',
    'ValidationError',
    'ResponseError',
]


class BaseError(Exception):
    msg = None

    def __init__(self, msg=None):
        super(BaseError, self).__init__()
        if msg is not None:
            self.msg = msg

    def __str__(self):
        return self.msg


class RequestError(BaseError):
    pass


class ValidationError(RequestError):
    msg = "Invalid request data."


class ValidationErrorDefault(ValidationError):
    def __init__(self, default, *args, **kwargs):
        super(ValidationErrorDefault, self).__init__(*args, **kwargs)
        self.default = default


class ResponseError(BaseError):
    """Exception for Ubersmith API Response.

        msg: optional message to pass along w/ stacktrace
        response: decoded json response w/ error info

    """
    msg = "Error in response from Ubersmith API."

    def __init__(self, msg=None, response=None):
        super(ResponseError, self).__init__(msg)
        if response is None:
            response = {}
        self.response = response
        self.error_code = response.get('error_code')
        self.error_message = response.get('error_message')
        self.msg = '{0.msg} {0.error_code} {0.error_message}'.format(self)
