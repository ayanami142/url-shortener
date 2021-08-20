from flask import Flask, redirect, request

from shortener import UrlShortener

app = Flask(__name__)
shortener = UrlShortener()


@app.route("/shorten_url", methods=["POST"])
def shorten_url():
    content = request.json
    url = content.get("url")
    shortener.check_url_and_raise_errors(url)
    url_code = shortener.shorten(url)
    full_url = request.host_url + url_code
    return {"shortened_url": full_url}


@app.route("/<shorten>", methods=["GET"])
def redirect_to_url(shorten: str):
    base_url = shortener.shorten_to_url(shorten)
    if not base_url:
        shortener.raise_error("Invalid short code", 400)

    # check if url starts with http or https and add that to url because Flask can not redirect
    # outside the application without that protocols
    if not base_url.startswith(("http:", "https:")):
        base_url = "https://" + base_url
    return redirect(base_url)


if __name__ == "__main__":
    app.run(threaded=3)
