from streamlike.exceptions import *

def get_errors_from_json(json):
    return json['errors'][0]['error']['message']

def raise_errors_on_failure(response):
    if response.status_code == 404:
        raise ResourceNotFound("Not found.")
    elif response.status_code == 400 or response.status_code == 406:
        raise BadRequest(get_errors_from_json(response.json()))
    elif response.status_code == 401:
        raise AuthenticationError(get_errors_from_json(response.json()))
    elif response.status_code == 413:
        raise RequestTooLarge(get_errors_from_json(response.json()))
    elif response.status_code == 415:
        raise FileTypeUnsupported(get_errors_from_json(response.json()))
    elif response.status_code == 429:
        raise TooManyRequests(rget_errors_from_json(response.json()))
    elif response.status_code == 500:
        raise ServerError(get_errors_from_json(response.json()))
    elif response.status_code == 502:
        raise BadGatewayError(get_errors_from_json(response.json()))
    elif response.status_code == 503:
        raise ServiceUnavailableError(get_errors_from_json(response.json()))
