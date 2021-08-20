from flask import make_response, jsonify, abort

from consts import REDIS_HOST, REDIS_PORT, URL_REGEX
import redis
import base64
from redis.exceptions import ConnectionError


class UrlShortener:
    """Convert url to shorten or get full url from shorten"""

    def __init__(self):
        self.r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0,
            charset="utf-8",
            decode_responses=True,  # convert from bytes to string automatically
        )

    def shorten(self, url: str) -> str:
        """
        Convert url to shorten and set data to redis
        :param str url: Url from request
        :return str: shorten url
        """
        short_url = self._generate_random_string(url)
        self.r.set(short_url, url)
        return short_url

    def shorten_to_url(self, code: str) -> str:
        """
        Convert shorten url to full url
        :param str code: url uuid
        :return str: full url
        """
        return self.r.get(code)

    @staticmethod
    def _generate_random_string(url: str, length: int = 8) -> str:
        """
        Generate random string from ascii letters and digits
        :param str url: url from request
        :param int length: length of random string, 8 by default
        :return str: generated string
        """
        byte_url = url.encode("UTF-8")
        return base64.b64encode(byte_url).decode("UTF-8")[:length]

    @staticmethod
    def raise_error(msg: str, code: int = 400) -> None:
        """
        Raise an error with message and status code in json format
        :param str msg: text of message
        :param int code: status code
        :return None:
        """
        response = make_response(jsonify(message=msg), code)
        abort(response)

    def check_url_and_raise_errors(self, url: str) -> bool:
        """Check if url is valid or raise an error
        Valid url examples:
            https://www.domain.dom:5000/hello
            www.test.test
            google.com
            localhost
        :param str url: url from request
        :return bool: valid or not valid
        """
        if not url:
            self.raise_error("Url can not be empty", 400)

        try:
            return URL_REGEX.match(url).span()[1] - URL_REGEX.match(url).span()[0] == len(url)
        except AttributeError:
            self.raise_error("Url should be valid", 400)
