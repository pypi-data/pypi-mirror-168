from __future__ import annotations

import uuid
import typing
import itertools
import collections
from datetime import datetime

import naming
try:
    from pxr import Sdf
    _USD_SUFFIXES = tuple(ext for ext in Sdf.FileFormat.FindAllFileFormatExtensions() if ext.startswith('usd'))
except ImportError:  # Don't fail if Sdf is not importable to facilitate portability
    _USD_SUFFIXES = ("usd", "usda", "usdc", "usdz", "usdt")

from grill.tokens import ids


def _table_from_id(token_ids):
    headers = [
        'Token',
        'Pattern',
        'Default',
        'Description',
    ]
    table_sep = tuple([''] * len(headers))
    sorter = lambda value: (
        # cleanup backslashes formatting
        value.pattern.replace('\\', '\\\\'),
        value.default,
        # replace new lines with empty strings to avoid malformed tables.
        value.description.replace('\n', ' '),
    )
    rows = [table_sep, headers, table_sep]
    rows.extend([token.name, *sorter(token.value)] for token in token_ids)
    rows.append(table_sep)
    max_sizes = [(max(len(i) for i in r)) for r in zip(*rows)]

    format_rows = []
    for r in rows:
        filler = '=<' if r == table_sep else ''
        format_rows.append(' '.join(
            f"{{:{f'{filler}'}{f'{size}'}}}".format(i)
            for size, i in zip(max_sizes, r))
        )
    return '\n'.join(format_rows)


class DefaultName(naming.Name):
    """ Inherited by: :class:`grill.names.CGAsset`

    Base class for any Name object that wishes to provide `default` functionality via
    the `get_default` method.

    Subclass implementations can override the `_defaults` member to return a mapping
    appropriate to that class.
    """
    _defaults = {}

    @classmethod
    def get_default(cls, **kwargs) -> DefaultName:
        """Get a new Name object with default values and overrides from **kwargs."""
        name = cls()
        defaults = dict(name._defaults, **kwargs)
        name.name = name.get(**defaults)
        return name


class DefaultFile(DefaultName, naming.File):
    """ Inherited by: :class:`grill.names.DateTimeFile`

    Similar to :class:`grill.names.DefaultName`, provides File Name objects default
    creation via the `get_default` method.

    Adds an extra `DEFAULT_SUFFIX='ext'` member that will be used when creating objects.
    """

    DEFAULT_SUFFIX = 'ext'

    @property
    def _defaults(self):
        result = super()._defaults
        result['suffix'] = type(self).DEFAULT_SUFFIX
        return result


class DateTimeFile(DefaultFile):
    """Time based file names respecting iso standard.

    ============= ================
    **Config:**
    ------------------------------
    *year*        Between :py:data:`datetime.MINYEAR` and :py:data:`datetime.MAXYEAR` inclusive.
    *month*       Between 1 and 12 inclusive.
    *day*         Between 1 and the number of days in the given month of the given year.
    *hour*        In ``range(24)``.
    *minute*      In ``range(60)``.
    *second*      In ``range(60)``.
    *microsecond* In ``range(1000000)``.
    ============= ================

    ======  ============
    **Composed Fields:**
    --------------------
    *date*  `year` `month` `day`
    *time*  `hour` `minute` `second` `microsecond`
    ======  ============

    .. note::
        When getting a new default name, current ISO time at the moment of execution is used.

    Example:
        >>> tf = DateTimeFile.get_default(suffix='txt')
        >>> tf.day
        '28'
        >>> tf.date
        '2019-10-28'
        >>> tf.year = 1999
        >>> tf
        DateTimeFile("1999-10-28 22-29-31-926548.txt")
        >>> tf.month = 14  # ISO format validation
        Traceback (most recent call last):
            ...
        ValueError: month must be in 1..12
        >>> tf.datetime
        datetime.datetime(1999, 10, 28, 22, 29, 31, 926548)
    """

    config = dict.fromkeys(
        ('month', 'day', 'hour', 'minute', 'second'), r'\d{1,2}'
    )
    config.update(year=r'\d{1,4}', microsecond=r'\d{1,6}')
    join = dict(
        date=('year', 'month', 'day'),
        time=('hour', 'minute', 'second', 'microsecond'),
    )
    join_sep = '-'

    @property
    def _defaults(self):
        result = super()._defaults
        time_field = {'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'}
        now = datetime.now()
        result.update({f: getattr(now, f) for f in time_field})
        return result

    def get_pattern_list(self) -> typing.List[str]:
        """Fields / properties names (sorted) to be used when building names.

        Defaults to [`date`, `time`] + keys of this name's config
        """
        return ["date", "time"] + super().get_pattern_list()

    @property
    def name(self) -> str:
        return super().name

    @name.setter
    def name(self, name: str):
        prev_name = self._name
        super(DateTimeFile, self.__class__).name.fset(self, name)
        if name:
            try:  # validate via datetime conversion
                self.datetime
            except ValueError:
                if prev_name:  # if we had a previous valid name, revert to it
                    self.name = prev_name
                raise

    @property
    def datetime(self) -> datetime:
        """ Return a :py:class:`datetime.datetime` object using this name values.

            >>> tf = DateTimeFile("1999-10-28 22-29-31-926548.txt")
            >>> tf.datetime
            datetime.datetime(1999, 10, 28, 22, 29, 31, 926548)
        """
        if not self.name:
            raise AttributeError("Can not retrieve datetime from an empty name")
        date = f"{int(self.year):04d}-{int(self.month):02d}-{int(self.day):02d}"
        time = (f"{int(self.hour):02d}:{int(self.minute):02d}:{int(self.second):02d}."
                f"{int(self.microsecond):06d}")
        return datetime.fromisoformat(f'{date}T{time}')


class CGAsset(DefaultName):
    """Inherited by: :class:`grill.names.CGAssetFile`

    Elemental resources that, when composed, generate the entities that bring an idea to a tangible product
    through their life cycles (e.g. a character, a film, a videogame).

    """
    config = {token.name: token.value.pattern for token in ids.CGAsset}
    __doc__ += '\n' + _table_from_id(ids.CGAsset) + '\n'

    def __init__(self, *args, sep='-', **kwargs):
        super().__init__(*args, sep=sep, **kwargs)

    @property
    def _defaults(self):
        result = super()._defaults
        result.update({token.name: token.value.default for token in ids.CGAsset})
        return result


class CGAssetFile(CGAsset, DefaultFile, naming.PipeFile):
    """Inherited by: :class:`grill.names.UsdAsset`

    Versioned files in the pipeline for a CGAsset.

    Example:
        >>> name = CGAssetFile.get_default(version=7)
        >>> name.suffix
        'ext'
        >>> name.suffix = 'abc'
        >>> name.path
        WindowsPath('demo/3d/abc/entity/rnd/lead/atom/main/all/whole/7/demo-3d-abc-entity-rnd-lead-atom-main-all-whole.7.abc')
    """

    @property
    def _defaults(self):
        result = super()._defaults
        result.update(version=1)
        return result

    def get_path_pattern_list(self) -> typing.List[str]:
        pattern = super().get_pattern_list()
        pattern.append('version')
        return pattern


class UsdAsset(CGAssetFile):
    """Specialized :class:`grill.names.CGAssetFile` name object for USD asset resources.

    .. admonition:: Inheritance Diagram for UsdAsset
        :class: dropdown, note

        .. inheritance-diagram:: grill.names.UsdAsset

    This is the currency for USD asset identifiers in the pipeline.

    Examples:
        >>> asset_id = UsdAsset.get_default()
        >>> asset_id
        UsdAsset("demo-3d-abc-entity-rnd-main-atom-lead-base-whole.1.usda")
        >>> asset_id.suffix = 'usdc'
        >>> asset_id.version = 42
        >>> asset_id
        UsdAsset("demo-3d-abc-entity-rnd-main-atom-lead-base-whole.42.usdc")
        >>> asset_id.suffix = 'abc'
        Traceback (most recent call last):
        ...
        ValueError: Can't set invalid name 'demo-3d-abc-entity-rnd-main-atom-lead-base-whole.42.abc' on UsdAsset("demo-3d-abc-entity-rnd-main-atom-lead-base-whole.42.usdc"). Valid convention is: '{code}-{media}-{kingdom}-{cluster}-{area}-{stream}-{item}-{step}-{variant}-{part}.{pipe}.{suffix}' with pattern: '^(?P<code>\w+)\-(?P<media>\w+)\-(?P<kingdom>\w+)\-(?P<cluster>\w+)\-(?P<area>\w+)\-(?P<stream>\w+)\-(?P<item>\w+)\-(?P<step>\w+)\-(?P<variant>\w+)\-(?P<part>\w+)(?P<pipe>(\.(?P<output>\w+))?\.(?P<version>\d+)(\.(?P<index>\d+))?)(\.(?P<suffix>sdf|usd|usda|usdc|usdz))$'

    .. seealso::
        :class:`grill.names.CGAsset` for a description of available fields, :class:`naming.Name` for an overview of the core API.

    """
    DEFAULT_SUFFIX = 'usd'
    file_config = naming.NameConfig(
        # NOTE: limit to only extensions starting with USD (some environments register other extensions untested by the grill)
        {'suffix': "|".join(_USD_SUFFIXES)}
    )

    @classmethod
    def get_anonymous(cls, **values) -> UsdAsset:
        """Get an anonymous :class:`UsdAsset` name with optional field overrides.

        Useful for situations where a temporary but valid identifier is needed.

        :param values: Variable keyword arguments with the keys referring to the name's
            fields which will use the given values.

        Example:
            >>> UsdAsset.get_anonymous(stream='test')
            UsdAsset("4209091047-34604-19646-169-123-test-4209091047-34604-19646-169.1.usda")

        """
        keys = cls.get_default().get_pattern_list()
        anon = itertools.cycle(uuid.uuid4().fields)
        return cls.get_default(**collections.ChainMap(values, dict(zip(keys, anon))))


class LifeTR(naming.Name):
    """Taxonomic Rank used for biological classification.

    """
    config = {token.name: token.value.pattern for token in ids.LifeTR}
    __doc__ += '\n' + _table_from_id(ids.LifeTR) + '\n'

    def __init__(self, *args, sep=':', **kwargs):
        super().__init__(*args, sep=sep, **kwargs)
