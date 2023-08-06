from werkzeug import exceptions as exception

__all__ = [
    "HTTPException",
    "NoContent",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "FailedDependency",
    "InternalServerError",
    "NotImplemented",
    "ServiceUnavailable",
]

# Notes on exceptions handling and errors:
# https://werkzeug.palletsprojects.com/en/master/exceptions/
# https://tools.ietf.org/html/rfc7807
HTTPException = exception.HTTPException

# 204 No Content
class NoContent(HTTPException):
    code = 204
    name = "No Content"


# 400 Bad Request
BadRequest = exception.BadRequest

# 401 Unauthorized
Unauthorized = exception.Unauthorized

# 403 Forbidden
Forbidden = exception.Forbidden

# 404 NotFound
NotFound = exception.NotFound

# 424 FailedDependency
FailedDependency = exception.FailedDependency

# 500 InternalServerError
InternalServerError = exception.InternalServerError

# 501 NotImplemented
# pylint: disable=redefined-builtin
NotImplemented = exception.NotImplemented

# 503 ServiceUnavailable
ServiceUnavailable = exception.ServiceUnavailable


class HTTPExceptions:
    pass


# Copy all symbols above into HTTPExceptions
for x in __all__:
    setattr(HTTPExceptions, x, locals()[x])
