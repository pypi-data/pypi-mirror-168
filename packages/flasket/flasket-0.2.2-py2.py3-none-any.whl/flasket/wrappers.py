from functools import wraps
from urllib.parse import urlparse

from flask import current_app

__all__ = ["endpoint", "require_http_same_origin"]


def endpoint(fn):
    """
    Decorate a function to pass 'app' to it
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        app = kwargs.pop("app", current_app.flasket)
        return fn(
            app=app,
            *args,
            **kwargs,
        )

    return wrapper


def require_http_same_origin(fn):
    """
    Decorator that requires the HTTP Referer to be the same
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        app = kwargs.pop("app", current_app.flasket)
        referer = app.request.headers.get("Referer")
        if not referer:
            raise app.Unauthorized("Unauthorized: Invalid referer")

        retval = urlparse(referer)
        referer = f"{retval.scheme}://{retval.netloc}"
        if referer != app.baseurl:
            raise app.Unauthorized("Unauthorized: Invalid referer")
        return fn(app=app, *args, **kwargs)

    return wrapper
