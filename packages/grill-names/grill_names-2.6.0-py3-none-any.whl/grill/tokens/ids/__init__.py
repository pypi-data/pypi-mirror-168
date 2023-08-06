import enum
import typing
import configparser
from importlib import resources
from functools import lru_cache


class _TokenID(typing.NamedTuple):
    description: str
    short_name: str
    pattern: str = r'\w+'
    default: str = ''


@lru_cache()
def __getattr__(name):
    cfg_fname = f'{name}.cfg'
    if resources.is_resource(__name__, cfg_fname):
        cfg = configparser.ConfigParser()
        cfg.read_string(resources.read_text(__name__, cfg_fname))
        return enum.Enum(name, ((s, _TokenID(**cfg[s])) for s in cfg.sections()))
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return tuple(
        # how to do better?
        c.split('.cfg')[0] for c in resources.contents(__name__) if c.endswith('.cfg')
    )
