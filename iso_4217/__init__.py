import enum
from typing import FrozenSet, Optional, Tuple

from . import lists

__version_prefix__ = "0.2"
__published_date__, _TABLE = lists.load()
__version__ = "{}.{:%y%m%d}".format(__version_prefix__, __published_date__)


def _generate_enum(locals):
    for k, v in _TABLE.items():
        locals[k] = (v.number, v.discriminator) if v.discriminator else v.number


class Currency(enum.Enum):
    """
    Represents distinct currency found in "Current currency & funds code"
    and "Codes for historic denominations of currencies & funds" lists.

    *Member name* is a 3-letter uppercase currency code
    *Member value* is the currency number or a tuple(currnency number, alias number).
    Alias number is there to distinguish historical currencies
    that share the same currency number.
    Some historical currencies have no currency number assigned to them.

    >>> Currency['EUR'].name
    'EUR'
    >>> Currency['EUR'].value
    978
    >>> Currency['XFU'].value
    (None, 3)
    >>> Currency.UYU
    <Currency.UYU: 858>
    >>> Currency.UYN
    <Currency.UYN: (858, 1)>

    """

    @property
    def number(self) -> Optional[int]:
        """
        Three-digit currency code number.
        Same as value except for historical currencies that might have their
        number reused and have tuple(currnency number, alias number)
        as value.

        >>> Currency.USD.number
        840
        >>> Currency.UYN.number
        858
        """
        return _TABLE[self.name].number

    @property
    def unit(self) -> str:
        """
        Name of the signle unit of the currency

        >>> Currency.CHF.unit
        'Swiss Franc'
        """
        return _TABLE[self.name].unit

    @property
    def entities(self) -> FrozenSet[str]:
        """
        Set of countries or other entities using the currency.
        Empty for historical currencies.
        :return: frozen set of entity names.

        >>> Currency.RUB.entities
        frozenset({'RUSSIAN FEDERATION (THE)'})
        >>> Currency.ECV.entities
        frozenset()
        """
        return _TABLE[self.name].entities

    @property
    def withdrew_entities(self) -> Tuple[Tuple[str, str], ...]:
        """
        Countries or other entities that do not use the currency anymore.
        :return: List of tuples of entities and dates when withdrawl happened.

        >>> Currency.UAK.withdrew_entities
        (('UKRAINE', '1996-09'),)
        """
        return _TABLE[self.name].withdrew_entities

    @property
    def is_fund(self) -> bool:
        """
        Currencies marked as funds.

        >>> Currency.USN.is_fund
        True
        """
        return _TABLE[self.name].is_fund

    @property
    def subunit_exp(self) -> Optional[int]:
        """
        Power of ten to produce amount of subunits in single currency unit
        :return: Number of digits after decimal point

        >>> Currency.BHD.subunit_exp
        3
        >>> Currency.USD.subunit_exp
        2
        >>> Currency.JPY.subunit_exp
        0
        """
        return _TABLE[self.name].subunit_exp

    def __str__(self):
        return self.name

    _generate_enum(locals())
