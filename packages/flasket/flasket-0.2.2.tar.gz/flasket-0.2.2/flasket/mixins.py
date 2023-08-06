# FIXME: rename to properties
import logging

import flask

from attr import define, field

from .exceptions import HTTPExceptions

__all__ = []


@define(kw_only=True, slots=False)
class LoggerProperties:
    @property
    def logger(self):
        return logging.getLogger("stderr")


@define(kw_only=True, slots=False)
class FlasketProperties(HTTPExceptions):
    #: Parent flasket application
    _flasket = field()

    # The class accesses fields that exist only
    # on the flasket class
    @property
    def debug(self) -> bool:
        return self._flasket._debug

    @property
    def production(self) -> bool:
        return self._flasket._production

    @property
    def config(self):
        return self._flasket._cfg

    @property
    def rootpath(self) -> str:
        return self._flasket._rootpath

    @property
    def clients(self) -> object:
        return self._flasket._clients

    @property
    def sitename(self) -> str:
        return self._flasket.sitename

    @property
    def host(self) -> str:
        return self._flasket.host

    @property
    def port(self) -> int:
        return self._flasket.port

    @property
    def baseurl(self) -> str:
        return self._flasket.baseurl


@define(kw_only=True, slots=False)
class FlaskProperties:
    _flask = field(default=None, init=False)

    @property
    def flask(self):
        return self._flask

    def __call__(self, environ: dict, start_response):
        return self._flask.wsgi_app(environ, start_response)

    @property
    def current_app(self):
        return flask.current_app

    @property
    def session(self):
        return flask.session

    @property
    def request(self):
        return flask.request

    @staticmethod
    def redirect(location, code=302):
        return flask.redirect(location, code=code)

    @staticmethod
    def make_response(*args):
        return flask.make_response(
            *args,
        )

    @staticmethod
    def render_template(template_name_or_list, **context):
        return flask.render_template(template_name_or_list, **context)
