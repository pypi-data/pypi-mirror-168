import functools
import typing as t

from attr import define, field
from flask import current_app, has_app_context

from ..mixins import LoggerProperties

__all__ = ["client"]

g_clients = {}


def client(name: str = None) -> t.Callable:
    fn = None
    if callable(name) and hasattr(name, "__name__"):
        fn = name
        name = fn.__name__

    def register_client(fn, name=None):
        if has_app_context():
            assert False, "flasket.client.__init__: Application has a context"
        else:
            g_clients[name] = fn

    @functools.wraps(fn)
    def wrapped(fn):
        nonlocal name

        register_client(fn, name)
        return fn

    if fn:
        register_client(fn, name)
    return wrapped


@define(kw_only=True)
class ClientFactory(LoggerProperties):
    _flasket = field()

    def __getattr__(self, name):
        self.logger.info(f"Creating client '{name}'...")
        fn = g_clients.get(name)
        if fn is None:
            self.logger.error(f"Client '{name}' is not registered.")
            raise TypeError(f"Client '{name}' does not exist")

        try:
            retval = fn(app=self._flasket, name=name)
            setattr(self.__class__, name, property(fget=lambda self: retval))
            return retval
        except Exception:
            self.logger.error(f"Client '{name}' could not be loaded.")
            raise
