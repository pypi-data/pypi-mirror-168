"""
Main application. It handles returning the WSGI application,
but also returning the potential services it can connect to and use.

On the OpenAPI side, it handles merging multiple yaml files into a single
specification before loading it.
"""

import logging
import os
import random
import string
import sys
import typing as t
import weakref

from attrs import define, field
from flask import Flask, current_app, g as flask_g
from flask_gordon.middleware import BeforeFirstCallMiddleware
from flask_gordon.middleware import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix as ProxyMiddleware

from .clients import ClientFactory
from .handlers import BaseHandler, handler
from .handlers.api import ApiHandler
from .handlers.app import AppHandler
from .handlers.static import StaticHandler
from .logger import Logger
from .templates import template_global, g_template_global
from .wrappers import endpoint

__all__ = ["Application"]


@template_global
@endpoint
def is_production(app):
    return app.production


@template_global
@endpoint
def is_debug(app):
    return app.debug


@handler
@define(kw_only=True)
class Application(BaseHandler):
    #: Root/Parent flasket application will be a reference to ourself
    _flasket = field(default=None, init=False)

    # Flask App 'handlers'
    # TODO: Allow additional handlers on __init__
    _handlers: t.Dict = field(default=None, init=False)
    _handlers_cls: t.List = field(default=[AppHandler, ApiHandler, StaticHandler], init=False)

    # Class variables have most properties defined
    # in FlasketProperties
    _cfg = field(default=None)
    _clients = field(default=None, init=False)

    # Paths
    _rootpath = field(default=None)
    _sys_rootpath = field(default=None, init=False)

    # Flags
    _production = field(default=False, init=False)
    _debug = field(default=False, init=False)

    # --------------------------------------------------------------------------
    def __attrs_post_init__(self) -> None:
        self._flasket = weakref.proxy(self)

        Logger.configure()
        self.logger.info("Creating a new Application...")

        # Handle production/debug flags
        self._production = self.config["server"].get("production", False)
        self._debug = self.config["server"].get("debug", False)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)

        # Initialize rootpath
        def add_to_syspath(path):
            if path not in sys.path:
                self.logger.info(f"Adding path '{path}' to sys.path to enable dynamic loading...")
                sys.path.insert(0, path)

        rootpath = self._rootpath or os.getcwd()
        self._rootpath = os.path.abspath(rootpath)
        if not os.path.exists(self._rootpath) or not os.path.isdir(self._rootpath):
            self.logger.error(f"Root path directory '{self._rootpath}' does not exist.")
            sys.exit(1)
        self.logger.info(f"Using root path '{self._rootpath}' for dynamic loading.")
        add_to_syspath(self._rootpath)

        # Initialize sys_rootpath if rootpath contains '/./'
        self._sys_rootpath = self._rootpath
        if rootpath.count("/./"):
            self._sys_rootpath = rootpath.rpartition("/./")[0]
            self._sys_rootpath = os.path.abspath(self._sys_rootpath)
            add_to_syspath(self._sys_rootpath)

        # Initialize a Flask app with no static nor template folders
        self.logger.info("Initializing root flasket.application...")
        self._flask = Flask(__name__, static_folder=None, template_folder=None)
        # Add 'flasket' to Flask app, so it's available via current_app
        self._flask.flasket = weakref.proxy(self)

        # Configuration comes from several locations:
        # - the command line arguments,
        # - the configuration file
        # - defaults
        #
        # Flask is also very flexible to where settings can come from.
        #
        # The most important variables, mostly to start/pre-configure the service
        # have already been set
        #
        # Set some new defaults
        self.flask.config["JSON_SORT_KEYS"] = False
        self.flask.config["TEMPLATES_AUTO_RELOAD"] = not self.production
        self.flask.config["EXPLAIN_TEMPLATE_LOADING"] = os.getenv("EXPLAIN_TEMPLATE_LOADING")

        # Copy our config down to flask config
        server = self.config["server"]
        for key, _ in self.flask.config.items():
            lkey = key.lower()
            if lkey in server:
                self.flask.config[key] = server[lkey]

        # https://flask.palletsprojects.com/en/2.2.x/config/
        self.flask.config["DEBUG"] = self.config["server"]["debug"]

        # Handle the secret session key if missing
        secret_key = self.flask.config["SECRET_KEY"]
        if not secret_key:
            self.flask.config["SECRET_KEY"] = "".join(random.choices(string.ascii_letters, k=20))
            self.logger.warning("Generated a random secret session key")

        # Load dynamic client loader
        self._clients = ClientFactory(flasket=weakref.proxy(self))

        # Load all handlers
        self._handlers = {}
        for cls in self._handlers_cls:  # pylint: disable=not-an-iterable
            handler = cls(flasket=weakref.proxy(self))
            self._handlers[handler.prefix] = handler

        # Queue the middlewares
        middleware = DispatcherMiddleware(self._handlers["/"], self._handlers)
        proxy = self.config["server"].get("proxy", {})
        if proxy:
            middleware = ProxyMiddleware(middleware, **proxy)
        middleware = BeforeFirstCallMiddleware(middleware, self.__before_first_call)
        self.flask._wsgi_app = self.flask.wsgi_app
        self.flask.wsgi_app = middleware

        # Load all jinja2 templates
        self.logger.info("Loading Jinja2 templates...")
        for name, fn in g_template_global.items():
            self.logger.debug(f"Loading Jinja2 template '{name}'...")
            self.add_template_global(fn, name)

    def _register_fake_route(self, handler):
        # And add 'flasket' to Flask app, so it's available via current_app
        handler.flask.flasket = weakref.proxy(self)
        handler.flask.before_request(Application.__before_request)
        handler.flask.after_request(Application.__after_request)

    @staticmethod
    def __before_first_call() -> None:
        Logger.disable()

    @staticmethod
    def __before_request() -> None:
        # Inject some variables available to templates
        flasket = current_app.flasket
        flask_g.flasket = flasket

    @staticmethod
    def __after_request(response) -> None:
        # This method is called after after_request, and for all routes
        flasket = current_app.flasket

        # Log the request
        Logger.log_request(flasket.request, response)
        return response

    # --------------------------------------------------------------------------
    def add_template_global(self, fn, name=None):
        for _, handler in self._handlers.items():
            handler.flask.add_template_global(fn, name)

    # --------------------------------------------------------------------------
    # Properties
    @property
    def sitename(self) -> str:
        if self.port == 80:
            return "http://%s" % self.host
        return "http://%s:%s" % (self.host, self.port)

    @property
    def host(self) -> str:
        return self.config["server"]["listen"]

    @property
    def port(self) -> int:
        return self.config["server"]["port"]

    @property
    def baseurl(self) -> str:
        """Returns expected baseurl {retval.scheme}://{retval.netloc}"""
        baseurl = self.config["server"].get("baseurl", None)
        if baseurl:
            return baseurl
        return self.sitename

    # --------------------------------------------------------------------------
    def run(self, *args, **kwargs):
        return self.flask.run(*args, **kwargs)

    @property
    def handlers(self):
        return self._handlers
