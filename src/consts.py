import os
import re

URL_REGEX = re.compile(
    r"(^https?://)?"  # http:// or https:// (I set it like optional argument if url hasn't http or https)
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
    r"localhost|"  # localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

URL_HOST_REGEX = "(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*"


SQLALCHEMY_DATABASE_PATH = os.path.abspath(os.path.join(__file__, "../.."))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLALCHEMY_DATABASE_PATH + "/app.db"
SQLALCHEMY_TEST_DATABASE_URI = "sqlite:///" + SQLALCHEMY_DATABASE_PATH + "/test.db"
