"""
Description
-----------

The :class:`flasket.middleware.gunicorn.FlasketCLI` class will enable you to quickly create
and run a Flasket application through the Gunicorn middleware.

It is composed of a :class:`~flasket.middleware.gunicorn.FlasketCmdline` and a
:class:`~flasket.cli.FlasketSettings`. This will enable the following default command line
arguments to be proposed:

.. program:: flasket

.. option:: -l HOST, --listen HOST

   The ip to listen on (default: localhost)

.. option:: -p PORT, --port PORT

   The port to listen on (default: 8080)

.. option:: -c CFGFILE, --cfgfile CFGFILE

   Use CFGFILE as configuration file, otherwise first file found in
   search path is used. (default search path: (...))

.. option:: --ui, --no-ui

   Enable the OpenAPI UI. Disable with :option:`--no-ui`. (default: enabled)

.. option::  -w WORKERS, --workers WORKERS

   Number of thread workers. (default: 0. If 0, cpu to use is (cpu_count * 2) with a maximum
   of 8; if negative, cpu to use is (cpu_count * 2) with no maximum.)

.. option::  --pidfile FILE

   A filename to use for the PID file. (default: none)

A configuration dictionary will be built from the command line arguments, the configuration
file if specified and found, and the Flasket defaults for missing parameters. This
configuration dictionary will be fed to the Flasket application on startup.

Classes
-------

FlasketCmdline
^^^^^^^^^^^^^^

.. autoclass:: FlasketCmdline
  :show-inheritance:
  :members: __call__, add_arguments, transform

FlasketCLI
^^^^^^^^^^

.. autoclass:: FlasketCLI
  :show-inheritance:
  :members: run

"""
import argparse
import logging
import multiprocessing
import typing as t

from attr import define, field

from flask.logging import default_handler
from gunicorn.app.base import BaseApplication
from torxtools.pathtools import expandpath

from .. import cli
from .. import Application


class GunicornApplication(BaseApplication):
    @staticmethod
    def _get_cpu_workers(workers: int) -> int:
        """
        Return the number of workers gunicorn should start with.
        Impose a max limit to avoid overloading the host.

        Parameters
        ----------
        workers: int

            number of workers configured

        Returns
        -------
        int
        """
        if workers > 0:
            return workers

        # Do not overload the host with a default value too large
        # if it's a container, it could report host cpus
        # TODO: respect OMP_NUM_THREADS / OMP_THREAD_LIMIT variables
        cpus = max((multiprocessing.cpu_count() * 2), 1)
        if workers == 0:
            return min(cpus, 8)
        return cpus

    # pylint: disable=abstract-method
    # http://docs.gunicorn.org/en/stable/custom.html
    def __init__(self, *args, cfg: t.Dict, rootpath: str = None, **kwargs) -> None:
        """
        Initialize a Flasket application, and configure Gunicorn

        Parameters
        ----------
        cfg: dict

            dictionary containing configuration for the application

        rootpath: str

            location from where to load packages
        """
        self._flasket = Application(*args, cfg=cfg, rootpath=rootpath, **kwargs)

        # Rework the configuration
        cfg = self._flasket.config["server"]
        cfg["workers"] = self._get_cpu_workers(cfg["workers"])
        self.options = {
            "bind": "%s:%s" % (cfg["listen"], cfg["port"]),
            "pidfile": expandpath(cfg.get("pidfile")),
            "workers": cfg["workers"],
            "accesslog": "/dev/null",
            "errorlog": "/dev/null",
        }

        self._flasket.logger.info(f"Starting {cfg['workers']} workers...")
        super().__init__()

        # Use the Flask logger to log identically between flask and gunicorn
        # We have to specify a null FileStream handler, we'll remove it on first call
        # by using the _gunicorn identifier
        logger = logging.getLogger("gunicorn.error")
        default_handler._gunicorn = False
        logger.addHandler(default_handler)

    def load_config(self) -> None:
        """
        Load Gunicorn configuration ourselves.
        """
        # Pass the configuration down to gunicorn.app.base.BaseApplication
        cfg = {k: v for k, v in self.options.items() if k in self.cfg.settings and v is not None}
        for k, v in cfg.items():
            self.cfg.set(k.lower(), v)

    def load(self) -> None:
        """
        Return our application instance.
        """
        return self._flasket


class FlasketCmdline(cli.FlasketCmdline):
    """
    Class that defines and parses the command line arguments for Gunicorn middleware FlasketCLI.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments.
        Passed value will be merged with the default factory configuration.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Adds Gunicorn middleware specific command line arguments :option:`--workers`, :option:`--pidfile`
        to the ArgumentParser.

        Parameters
        ----------
        parser: argparse.ArgumentParser

            a parser on which `add_argument` will be called

        Returns
        -------
        argparse.ArgumentParser
        """
        defaults = self._default_cfg

        workers = defaults["server"]["workers"]
        pidfile = defaults["server"]["pidfile"]
        if pidfile is None:
            pidfile = "none"

        # fmt: off
        parser.add_argument("-w", "--workers", metavar="WORKERS", type=int,
            help=f"Number of thread workers. (default: {workers}. If 0, cpu to use is (cpu_count * 2) with a maximum of 8; if negative, cpu to use is (cpu_count * 2) with no maximum.)")
        parser.add_argument("--pidfile", metavar="FILE", type=str,
            help=f"A filename to use for the PID file. (default: {pidfile})")
        # fmt: on
        return parser


@define(kw_only=True)
class FlasketCLI(cli.ABCFlasketCli):
    """
    Gunicorn middleware client class.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments and configuration.
        Passed value will be merged with the default factory configuration.

    settings_cfg: any, default: :class:`flasket.cli.FlasketSettings`

        Dictionary, or Callable that returns a dictionary for the settings arguments.

    cmdline_cfg: any, default: :class:`flasket.middleware.gunicorn.FlasketCmdline`

        Dictionary, or Callable that returns a dictionary for the command line arguments.
    """

    # fmt: off
    _cmdline_cfg: any = field(default=FlasketCmdline)
    _forced_cfg: t.Dict = field(default={"server": {"debug": False, "production": True, "gunicorn": True,}}, init=False)
    # fmt: on

    def _run(self, *args, cfg: t.Dict, rootpath: str = None, **kwargs) -> None:
        """
        Run the middleware

        Parameters
        ----------

        cfg: dict
            dictionary containing configuration for the application

        rootpath: str, default: None

            path of root location: where the 'api', 'htdocs' and 'app' directories will be served
        """
        GunicornApplication(*args, cfg=cfg, rootpath=rootpath, **kwargs).run()


class LocalCmdline(FlasketCmdline):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        # fmt: off
        parser.add_argument("rootpath", default=None, nargs="?",
            help="root path of the server.")
        # fmt: on
        return parser


def main():
    FlasketCLI(cmdline_cfg=LocalCmdline).run()


if __name__ == "__main__":
    main()
