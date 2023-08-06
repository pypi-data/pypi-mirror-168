import re


class BadRequestError(Exception):
    pass


class InternalServerError(Exception):
    pass


class InvalidArgumentError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


def check_response_status(response):
    try:
        status = response.status_code
    except Exception as exception:
        raise exception.__class__('Response does not have a status code. ' + exception.__str__()) from exception

    if status == 200:
        return True

    else:

        matches = re.findall(r'<p>(.+?)</p>', response.text, flags=re.DOTALL)
        error_msg = ""
        if matches:
            error_msg = matches[0]

        if status == 400:
            raise BadRequestError(error_msg)

        elif status == 401:
            raise UnauthorizedError(error_msg)

        elif status == 500:
            raise InternalServerError(error_msg)
