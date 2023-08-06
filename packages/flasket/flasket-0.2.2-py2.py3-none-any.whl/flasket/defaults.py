import os
import typing as t

from boltons.iterutils import unique_iter, flatten_iter
from xdg import XDG_CONFIG_DIRS

SERVER_CFGNAME: str = "flasket.yml"

SERVER_LISTEN: str = "localhost"
SERVER_PORT: int = 8080

# fmt: off
CFGFILE_SEARCH_PATHS: t.List[str] = list(unique_iter(flatten_iter(
[
    "./.{cfgname}",                # ./.flasket.yml
    "./{cfgname}",                 # ./flasket.yml
    "$XDG_CONFIG_HOME/{cfgname}",  # ~/.config/flasket.yml
    "~/.{cfgname}",                # ~/.flasket.yml
    [os.path.join(str(e), "{cfgname}") for e in XDG_CONFIG_DIRS],
    "/etc/{cfgname}",              # /etc/flasket.yml
])))
# fmt: on


def default_configuration(defaults: t.Dict = None) -> t.Dict:
    """
    Convenience function that returns defaults for arguments,
    and for configuration file

    Parameters
    ----------
    defaults: dict
        a dictionary containing default values.

    Returns
    -------
    dict:
        a dictionary
    """
    if defaults is None:
        defaults = {}
    if "server" not in defaults:
        defaults["server"] = {}

    # cf. src/middleware/__init__.py
    return {
        "cfgname": defaults.get("cfgname", SERVER_CFGNAME),
        "cfgfile_search_paths": defaults.get("cfgfile_search_paths", CFGFILE_SEARCH_PATHS),
        "server": {
            "rootpath": defaults.get("rootpath"),
            "description": defaults.get("description", "Flasket server"),
            "debug": defaults["server"].get("debug", False),
            "listen": defaults["server"].get("listen", SERVER_LISTEN),
            "port": defaults["server"].get("port", SERVER_PORT),
            "ui": defaults["server"].get("ui", True),
            "workers": defaults["server"].get("workers", 0),
            "pidfile": defaults["server"].get("pidfile", None),
            "proxy": {
                "x_for": defaults["server"].get("proxy", {}).get("x_for", 1),
                "x_proto": defaults["server"].get("proxy", {}).get("x_proto", 1),
                "x_host": defaults["server"].get("proxy", {}).get("x_host", 0),
                "x_port": defaults["server"].get("proxy", {}).get("x_port", 0),
                "x_prefix": defaults["server"].get("proxy", {}).get("x_prefix", 0),
            },
        },
    }
