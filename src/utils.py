from flask import abort, jsonify, make_response

from src.consts import URL_REGEX


def check_url_and_raise_errors(url: str) -> None:
    """Check if url is valid or raise an error
    Valid url examples:
        https://www.domain.dom:5000/hello
        www.test.test
        google.com
        localhost
    :param str url: url from request
    :return None
    """
    if not url:
        raise_error("Url can not be empty", 400)

    try:
        URL_REGEX.match(url).span()[1] - URL_REGEX.match(url).span()[0] == len(url)
    except AttributeError:
        raise_error("Url should be valid", 400)


def raise_error(msg: str, code: int = 400) -> None:
    """
    Raise an error with message and status code in json format
    :param str msg: text of message
    :param int code: status code
    :return None:
    """
    response = make_response(jsonify(message=msg), code)
    abort(response)
