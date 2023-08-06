"""
 Error Handler
"""


class CropinAPIError(Exception):
    """Invalid response from DataHub. Base class for more specific exceptions.

    Attributes
    ----------
    msg: str
        The error message.
    response: requests.Response
        The response from the server as a `requests.Response` object.
    """

    def __init__(self, msg="", response=None):
        self.msg = msg
        self.response = response

    def __str__(self):
        if self.response is None:
            return self.msg
        if self.response.reason:
            reason = " " + self.response.reason
        else:
            reason = ""
        return "HTTP status {}{}: {}".format(
            self.response.status_code,
            reason,
            ("\n" if "\n" in self.msg else "") + self.msg,
        )


class ServerError(CropinAPIError):
    """Error raised when the server responded in an unexpected manner, typically due to undergoing maintenance"""

    pass


class UnauthorizedError(CropinAPIError):
    """Error raised when attempting to retrieve a product with incorrect credentials"""

    def __str__(self):
        return self.msg


class InvalidInputError(CropinAPIError):
    """Error raised when attempting to retrieve a product with incorrect credentials"""

    def __str__(self):
        return self.msg


class QuerySyntaxError(CropinAPIError, SyntaxError):
    """Error raised when the query string could not be parsed on the server side"""

    def __init__(self, msg, response):
        CropinAPIError.__init__(self, msg, response)
        SyntaxError.__init__(self, msg)

    def __str__(self):
        return self.msg


class QueryLengthError(CropinAPIError):
    """Error raised when the query string length was excessively long"""

    def __str__(self):
        return self.msg


class InvalidKeyError(CropinAPIError, KeyError):
    """Error raised when product with given key was not found on the server"""

    def __init__(self, msg, response):
        CropinAPIError.__init__(self, msg, response)
        KeyError.__init__(self, msg)

    def __str__(self):
        return self.msg
