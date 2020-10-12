import enum
from typing import FrozenSet, Optional, Tuple

from .lists import load_lists

__version_prefix__ = "0.1"
__published_date__, _TABLE = load_lists()
__version__ = "{}.{:%y%m%d}".format(__version_prefix__, __published_date__)


def _generate_enum(locals):
    for k, v in _TABLE.items():
        locals[k] = v.pop("number")


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
    def full_name(self) -> str:
        """
        Name of the currency

        >>> Currency.CHF.full_name
        'Swiss Franc'
        """
        return _TABLE[self.name]["name"]

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
        return _TABLE[self.name]["entities"]

    @property
    def withdrawn_entities(self) -> Tuple[Tuple[str, str], ...]:
        """
        Countries or other entities that do not use the currency anymore.
        :return: List of tuples of entities and dates when withdrawl happened.

        >>> Currency.UAK.withdrawn_entities
        (('UKRAINE', '1996-09'),)
        """
        return _TABLE[self.name]["withdrawn_entities"]

    @property
    def is_fund(self) -> bool:
        """
        Currencies marked as funds.

        >>> Currency.USN.is_fund
        True
        """
        return _TABLE[self.name]["is_fund"]

    @property
    def units(self) -> Optional[int]:
        """
        Minor currency units.
        :return: Number of digits after decimal point

        >>> Currency.BHD.units
        3
        >>> Currency.USD.units
        2
        >>> Currency.JPY.units
        0
        """
        return _TABLE[self.name]["units"]

    _generate_enum(locals())
