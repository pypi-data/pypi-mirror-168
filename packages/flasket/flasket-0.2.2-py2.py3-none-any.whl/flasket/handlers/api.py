import collections
import os
import sys
import traceback
import typing as t

from copy import deepcopy

import yaml

from attrs import define, field

from boltons.fileutils import iter_find_files
from connexion import FlaskApp
from connexion.exceptions import InvalidSpecification
from connexion.resolver import RestyResolver

from .. import utils as dicts
from . import Handler, handler

# TODO: Allow dynamic reload of api


class AutoResolver(RestyResolver):
    def resolve_operation_id_using_rest_semantics(self, operation):
        retval = super().resolve_operation_id_using_rest_semantics(operation)
        retval = retval.replace("api.api.", "api.", 1)
        return retval


def _load_yamlfiles(files: t.List[str]) -> t.Dict:
    """
    For every yaml file, load the file and merge with previous

    Parameters
    ----------
    files: List[str]
        list of files to parse and merge

    Returns
    -------
    dict:
        merged dictionary
    """
    try:
        data = {}
        for f in files:
            with open(f, "r", encoding="UTF-8") as fd:
                newdata = yaml.safe_load(fd)
            if newdata:
                data = dicts.deepmerge(data, newdata)
        return data
    except yaml.scanner.ScannerError as err:
        raise type(err)(
            f"yaml scanner error: {err.problem} in '{err.problem_mark.name}', at line {err.problem_mark.line}"
        ) from err
    except yaml.parser.ParserError as err:
        raise type(err)(
            f"yaml parser error: {err.problem} in '{err.problem_mark.name}', at line {err.problem_mark.line}"
        ) from err
    except Exception as err:
        raise type(err)(f"{str(err)} in file {f}") from err


def _find_yamlfiles(paths: t.List[str], logger: object) -> collections.OrderedDict:
    """
    Find all yaml files in paths, returns a merged dict

    Parameters
    ----------
    paths: List[str]
        list of paths to search

    Returns
    -------
    dict:
        merged dictionary
    """
    # Make paths unique but keep order
    paths = list(dict.fromkeys(paths))

    # Merge all yml files from the directory
    files = []
    for path in paths:
        if os.path.exists(path):
            if logger:
                logger.info(f"Reading OpenAPI files from '{path}'...")
            files.extend(iter_find_files(path, ["*.yml", "*.yaml"]))

    # Load the contents
    data = _load_yamlfiles(files)

    # sort the keys in /components/schemas, since the UI uses that order
    data["components"]["schemas"] = collections.OrderedDict(
        sorted((data["components"]["schemas"]).items(), key=lambda s: s[0].lower())
    )
    return data


def _remove_path_if_key(specs: t.Dict, key: str, value: str) -> t.Dict:
    """
    For every API path in specs, remove it if we find specs[...][key] = value

    Parameters
    ----------
    specs: Dict
        OpenAPI specs

    key: str
        Key to look for

    value: str
        Value to look for

    Returns
    -------
    dict:
        OpenAPI specs without the removed keys
    """
    rv = deepcopy(specs)
    for path in specs.get("paths", {}).keys():
        for method in specs["paths"][path].keys():
            if key not in specs["paths"][path][method]:
                continue
            if specs["paths"][path][method][key] == value:
                del rv["paths"][path][method]
    return rv


@handler
@define(kw_only=True)
class ApiHandler(Handler):
    _connexion = field(init=False, default=None)
    _api_rootpath: str = field(init=False, default=None)

    @property
    def prefix(self) -> str:
        return "/api"

    def __attrs_post_init__(self) -> None:
        self._api_rootpath = os.path.join(self.rootpath, "api")
        if not os.path.exists(self._api_rootpath):
            self.logger.warning("Directory 'api' in root path does not exist.")

        # Build specs from yml files, and remove debug endpoints
        specpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api"))
        specs = _find_yamlfiles([specpath, self._api_rootpath], self.logger)
        if not self.debug:
            specs = _remove_path_if_key(specs, "x-debug", True)

        # https://connexion.readthedocs.io/en/latest/
        # TODO: When spec "servers.url" is set, then we should
        # mangle parameters passed here to handle paths prefixed by '/api'
        self._connexion = FlaskApp(
            __name__,
            specification_dir="api",
        )
        try:
            self._connexion.add_api(
                specs,
                # base_path='/api',
                resolver=AutoResolver("api", "get"),
                strict_validation=True,
                validate_responses=True,
                options={
                    "openapi_spec_path": "/api/openapi.json",
                    "swagger_url": "/api/ui",
                    "swagger_ui": self.config["server"]["ui"],
                    "swagger_spec": self.config["server"]["ui"],
                },
            )
        except InvalidSpecification as err:
            raise type(err)(f"OpenAPI error: {err.message}") from err
        except Exception:
            # TODO: improve on this (make import error for example)
            print(traceback.print_exc(), file=sys.stderr)
            raise

        if self.config["server"]["ui"]:
            self.logger.info("Swagger UI is available at: %s%s", self.sitename, "/api/ui")
        else:
            self.logger.info("Swagger UI not started")

    @property
    def flask(self):
        return self._connexion.app

    def __call__(self, environ: dict, start_response):
        return self._connexion(environ, start_response)
