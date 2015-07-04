class StreamlikeException(Exception):
    """ Base error. """
    def __init__(self, message, result=None):
        super(StreamlikeException, self).__init__(message)
        self.result = result

class BadRequest(StreamlikeException):
    pass

class AuthenticationError(StreamlikeException):
    pass

class BadGatewayError(StreamlikeException):
    pass

class ResourceNotFound(StreamlikeException):
    pass

class ServerError(StreamlikeException):
    pass

class ServiceUnavailableError(StreamlikeException):
    pass

class RequestTooLarge(StreamlikeException):
    pass

class FileTypeUnsupported(StreamlikeException):
    pass

class UnprocessableEntity(StreamlikeException):
    pass

class TooManyRequests(StreamlikeException):
    pass

def raise_errors_on_failure(response):
    if response.status_code == 404:
        raise ResourceNotFound("Not found.")
    elif response.status_code == 400 or response.status_code == 406:
        raise BadRequest("Incoming request body does not contain a valid JSON object.")
    elif response.status_code == 401:
        raise AuthenticationError("Unnknown API Key. Please check your API key and try again")
    elif response.status_code == 413:
        raise RequestTooLarge("File size too large.")
    elif response.status_code == 415:
        raise FileTypeUnsupported("File type not supported.")
    elif response.status_code == 429:
        raise TooManyRequests("Overage usage limit hit.")
    elif response.status_code == 500:
        raise ServerError("Server has encountered an unexpected error and cannot fulfill your request")
    elif response.status_code == 502:
        raise BadGatewayError("Bad gateway.")
    elif response.status_code == 503:
        raise ServiceUnavailableError("Service unavailable.")

    return response