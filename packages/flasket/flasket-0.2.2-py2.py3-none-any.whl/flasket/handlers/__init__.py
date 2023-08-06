import functools

from attrs import define

from ..mixins import FlasketProperties, FlaskProperties, LoggerProperties

__all__ = []


def handler(cls):
    @functools.wraps(cls, updated=())
    class Wrapper(cls):
        def __attrs_post_init__(self):
            super().__attrs_post_init__()
            super().__post_init__()

    return Wrapper


class BaseHandler(FlasketProperties, FlaskProperties, LoggerProperties):
    def __post_init__(self) -> None:
        # Register a route to always call before/after_app_request
        self._flasket._register_fake_route(handler=self)


class Handler(BaseHandler):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.flask.flasket = self.flasket
        self._copy_configuration()

    def _copy_configuration(self):
        for key, value in self.flasket.flask.config.items():
            self.flask.config[key] = value

    @property
    def flasket(self):
        return self._flasket
