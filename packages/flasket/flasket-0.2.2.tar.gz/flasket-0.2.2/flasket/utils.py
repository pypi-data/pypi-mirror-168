# FIXME: get rid of this file?
import os

from copy import deepcopy

from boltons.iterutils import remap

from torxtools.dicttools import _deepmerge, strip_none

## TODO: Use torxtools.deepmerge
def deepmerge(dest, src):
    """
    Take every key, value from src and merge it recursivly into dest.
    None values are stripped from src before merging.

    Adapted from https://stackoverflow.com/questions/7204805

    Parameters
    ----------
    dest: dict
        destination dictionary

    src: dict
        source dictionary

    Returns
    -------
    dict:
        merged dictionary
    """
    # pylint: disable=unnecessary-lambda-assignment
    src = remap(src, visit=strip_none)

    return _deepmerge(src, deepcopy(dest))


def get_module_name(filepath: str, syspath: str) -> str:
    filepath = os.path.relpath(filepath, syspath)
    return filepath.replace("/", ".").replace(".py", "")
