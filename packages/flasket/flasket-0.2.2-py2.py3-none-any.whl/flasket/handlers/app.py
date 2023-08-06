import os

from pydoc import importfile

from flask import Flask, Blueprint

from attrs import define, field

from boltons.fileutils import iter_find_files

from . import Handler, handler
from ..utils import get_module_name


@handler
@define(kw_only=True)
class AppHandler(Handler):
    _app_rootpath: str = field(init=False, default=None)
    _modules = field(init=False, default=None)

    @property
    def prefix(self) -> str:
        return "/app"

    def __attrs_post_init__(self) -> None:
        self._modules = {}

        # FIXME: api are referenced as api.xyz.get, but app templates as xyz.get only
        self._app_rootpath = os.path.join(self.rootpath, "app")
        if not os.path.exists(self._app_rootpath):
            self.logger.warning("Directory 'app' in root path does not exist.")

        # Load all ./app/**/*.py
        files = iter_find_files(self._app_rootpath, ["*.py"])
        for f in files:
            self._load_module(f)

        ## TODO: Allow serving of html files via the template rendering module
        # Use None for static_folder to prevent adding a automatic "/<filename>" route
        self._flask = Flask(__name__, root_path=self._app_rootpath, static_folder=None, template_folder=None)
        blueprint = Blueprint(
            "app",
            __name__,
            root_path=self._app_rootpath,
            static_folder=None,
            template_folder=self._app_rootpath,
        )

        blueprint.add_url_rule("/app/", view_func=self.send_file)
        blueprint.add_url_rule("/app/<path:path>", view_func=self.send_file)
        self.flask.register_blueprint(blueprint)

        self.flask.jinja_env.trim_blocks = True
        self.flask.jinja_env.lstrip_blocks = True

    def send_file(self, path: str = "") -> object:
        # TODO: Allow sending html files without and associated python file
        filepath = os.path.join(self._app_rootpath, path)

        # FIXME: use __init__.py? and not index.py?
        if path == "" or path[-1:] == "/":
            filepath += "index"
        filepath += ".py"

        if not os.path.exists(filepath):
            raise self.NotFound

        ## TODO: allow all methods
        module = self._load_module(filepath)
        return module.get(app=self.flasket, path=path)

    @staticmethod
    def _load_module_by_filepath(filepath: str) -> object:
        ## TODO: Add error handling
        return importfile(filepath)

    def _load_module(self, filepath: str) -> object:
        # Prepare a fake module name, we'll load by file
        refresh = not self.production
        module_name = get_module_name(filepath, self._app_rootpath)

        # If we already have it and won't reload, send it back now
        exists = module_name in self._modules
        if exists and not refresh:
            return self._modules[module_name]["module"]

        # Load once if never loaded before
        if not exists:
            module = self._load_module_by_filepath(filepath)
            if module is None:
                raise self.InternalServerError

            # Add to our array
            mtime = os.stat(filepath).st_mtime
            self._modules[module_name] = {"module": module, "mtime": mtime}
            return module

        # Possibly reload
        item = self._modules[module_name]
        mtime = os.stat(filepath).st_mtime
        if mtime == item["mtime"]:
            return item["module"]
        del self._modules[module_name]
        return self._load_module(filepath)
