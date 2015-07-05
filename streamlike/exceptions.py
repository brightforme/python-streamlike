#TODO: Are they really needed?
class StreamlikeException(Exception):
    """ Base error. """
    def __init__(self, message, result=None):
        super(StreamlikeException, self).__init__(message)
        self.result = result

class BadRequest(StreamlikeException):
    """Signifies HTTP codes 400 or 406"""
    pass

class AuthenticationError(StreamlikeException):
    """Signifies HTTP code 401"""
    pass

class ResourceNotFound(StreamlikeException):
    """Signifies HTTP code 404"""
    pass

class RequestTooLarge(StreamlikeException):
    """Signifies HTTP code 413"""
    pass

class FileTypeUnsupported(StreamlikeException):
    """Signifies HTTP code 415"""
    pass

class TooManyRequests(StreamlikeException):
    """Signifies HTTP code 429"""
    pass

class ServerError(StreamlikeException):
    """Signifies HTTP code 500"""
    pass

class BadGatewayError(StreamlikeException):
    """Signifies HTTP code 502"""
    pass

class ServiceUnavailableError(StreamlikeException):
    """Signifies HTTP code 503"""
    pass
