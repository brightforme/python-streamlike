"""An internal(!) helpers module"""
from streamlike.exceptions import *

def get_error_from_json(json):
    """
        Parses the json and returns the error message.

        json -- a json object containg the response by the API

        returns -- the error string contained in the response
    """
    return json['errors'][0]['error']['message']

def raise_errors_on_failure(response):
    """
        Given an API response, either throws an appropriate
        exception when the response errored or return the result.

        response -- the response to check
    """
    msg = ""
    if response.status_code != 200:
        msg = get_error_from_json(response.json())

    if response.status_code == 404:
        raise ResourceNotFound("Not found.")
    elif response.status_code == 400 or response.status_code == 406:
        raise BadRequest(msg)
    elif response.status_code == 401:
        raise AuthenticationError(msg)
    elif response.status_code == 413:
        raise RequestTooLarge(msg)
    elif response.status_code == 415:
        raise FileTypeUnsupported(msg)
    elif response.status_code == 429:
        raise TooManyRequests(msg)
    elif response.status_code == 500:
        raise ServerError(msg)
    elif response.status_code == 502:
        raise BadGatewayError(msg)
    elif response.status_code == 503:
        raise ServiceUnavailableError(msg)
