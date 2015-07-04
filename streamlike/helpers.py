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
        raise BadRequest(response.json()['errors'][0]['error']['message'])
    elif response.status_code == 401:
        raise AuthenticationError(response.json()['errors'][0]['error']['message'])
    elif response.status_code == 413:
        raise RequestTooLarge(response.json()['errors'][0]['error']['message'])
    elif response.status_code == 415:
        raise FileTypeUnsupported(response.json()['errors'][0]['error']['message'])
    elif response.status_code == 429:
        raise TooManyRequests(rresponse.json()['errors'][0]['error']['message'])
    elif response.status_code == 500:
        raise ServerError(response.json()['errors'][0]['error']['message'])
    elif response.status_code == 502:
        raise BadGatewayError(rresponse.json()['errors'][0]['error']['message'])
    elif response.status_code == 503:
        raise ServiceUnavailableError(response.json()['errors'][0]['error']['message'])

    return response