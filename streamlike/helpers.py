"""An internal(!) helpers module"""
class StreamlikeException(Exception):
    """ Base error. """
    code = None

    def __init__(self, message, result=None):
        super(StreamlikeException, self).__init__(message)
        self.result = result
        if message:
            self.message = message

class BadRequest(StreamlikeException):
    """Signifies HTTP codes 400 or 406"""
    code = 400

class AuthenticationError(StreamlikeException):
    """Signifies HTTP code 401"""
    code = 401

class ResourceNotFound(StreamlikeException):
    """Signifies HTTP code 404"""
    code = 404

class NotAcceptable(StreamlikeException):
    """Signifies HTTP code 406"""
    code = 406

class RequestTooLarge(StreamlikeException):
    """Signifies HTTP code 413"""
    code = 413

class FileTypeUnsupported(StreamlikeException):
    """Signifies HTTP code 415"""
    code = 415

class TooManyRequests(StreamlikeException):
    """Signifies HTTP code 429"""
    code = 429

class ServerError(StreamlikeException):
    """Signifies HTTP code 500"""
    code = 500
    message = "Internal Server Error"

class BadGatewayError(StreamlikeException):
    """Signifies HTTP code 502"""
    code = 502
    message = "Bad Gateway"

class ServiceUnavailableError(StreamlikeException):
    """Signifies HTTP code 503"""
    code = 503
    message = "Service is unavailable"

def get_error(response):
    try:
        json = response.json()
        if "message" in json:
            return json['message']
        if "error" in json:
            return json["error"]
    except ValueError:
        pass

    return ''


def raise_errors_on_failure(response):
    if response.status_code >= 400:
        msg = get_error(response)
        search_for_exception(response.status_code, msg)

    return response

# The code that follows is stolen from werkzeug:
# https://github.com/mitsuhiko/werkzeug/blob/d4e8b3f46c51e7374388791282e66323f64b3068/werkzeug/exceptions.py

_exceptions = {}
__all__ = ['StreamlikeException',
           'raise_errors_on_failure']

def _find_exceptions():
    for name, obj in globals().items():
        try:
            is_http_exception = issubclass(obj, StreamlikeException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.code is None:
            continue
        __all__.append(obj.__name__)
        old_obj = _exceptions.get(obj.code, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        _exceptions[obj.code] = obj

_find_exceptions()
del _find_exceptions

def search_for_exception(code, msg):
        if code not in _exceptions:
            raise LookupError('no exception for %r' % code)
        raise _exceptions[code](msg)