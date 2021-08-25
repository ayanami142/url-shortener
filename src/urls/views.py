from flask import Blueprint, redirect, request

from src.db import db
from src.utils import check_url_and_raise_errors, raise_error

from .models import Url, View

mod = Blueprint("shortener", __name__)


@mod.route("/shorten_url", methods=["POST"])
def shorten_url():
    """
    Convert url to shorten
    :return dict: response with short url
    """

    # get url from post request
    content = request.json
    base_url = content.get("url")
    check_url_and_raise_errors(base_url)

    # use existing url...
    url: Url = Url.query.filter_by(base_address=base_url).first()
    if url:
        short_url = url.id
    else:  # ... or create new instance
        url = Url(base_address=base_url)
        short_url = url.generate_short_url()
        url.id = short_url
        db.session.add(url)
        db.session.commit()

    # add view instance to url
    url.add_view_if_not_exists(ip=request.remote_addr)

    full_url = request.host_url + short_url

    return {"shortened_url": full_url}, 201


@mod.route("/<shorten>", methods=["GET"])
def redirect_to_url(shorten: str):
    """
    Convert shorten url to base url and redirect to this url
    :param shorten: uuid from url
    :return None or tuple: redirect to url or raise error with status 400
    """
    base_url: Url = Url.query.filter_by(id=shorten).first()
    if not base_url:
        raise_error("Short code was not found", 404)

    # check if url starts with http or https and add that to url because Flask can not redirect
    # outside the application without that protocols
    url = base_url.base_address
    if not url.startswith(("http:", "https:")):
        url = "https://" + url

    return redirect(url)


@mod.route("/shortened_urls_count", methods=["GET"])
def shortened_urls_count() -> tuple:
    """
    Count all views
    :return tuple: Text with number of shortened urls with status code
    """
    views_count: int = View.query.count()

    return {"Number of shortened urls": views_count}, 200


@mod.route("/top10", methods=["GET"])
def get_top_10() -> tuple:
    """
    Get top 10 urls
    :return tuple: urls separated by comma and ordered by views count
    """
    urls = (
        Url.query.outerjoin(View)
        .group_by(Url.id)
        .order_by(db.func.count(View.id).desc())
        .limit(10)
    )

    return {"Most popular urls": ", ".join(url.base_address for url in urls)}, 200
