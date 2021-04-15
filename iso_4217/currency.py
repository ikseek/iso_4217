import enum
from collections import defaultdict, deque
from typing import Dict, FrozenSet, Optional, Tuple

from .lists import Historic, load
from .pint import currency_unit

__published_date__, _TABLE = load()


def _generate_enum(locals: Dict) -> None:
    names = defaultdict(deque)
    for _, info in _TABLE.items():
        if info.entities:
            names[info.name].appendleft(info)
        else:
            names[info.name].append(info)
    renamed = {}
    for name, currencies in names.items():
        if currencies[0].entities:
            active = currencies.popleft()
            renamed[active.code] = name
        for historic in currencies:
            last_year = historic.withdrew_entities[-1].time.end.year
            renamed[historic.code] = "{} ({})".format(name, last_year)
    for name, value in renamed.items():
        locals[name] = value


class Currency(enum.Enum):
    """
    Represents distinct currency found in "Current currency & funds code"
    and "Codes for historic denominations of currencies & funds" lists.

    *Member name* is a 3-letter uppercase currency code
    *Member value* is currency name. Historical currencies have withdrawl year added
                   to the name to differentiate currencies that were withdrawn multiple
                   times.

    >>> Currency['EUR'].name
    'EUR'
    >>> Currency['EUR'].number
    978
    >>> Currency['XFU'].value
    'UIC-Franc (2013)'
    >>> Currency.UYU
    <Currency.UYU: 'Peso Uruguayo'>
    >>> Currency.UYN
    <Currency.UYN: 'Old Uruguay Peso (1989)'>
    """

    @property
    def number(self) -> Optional[int]:
        """
        Three-digit currency code number.
        Many historical currencies share same number.

        >>> Currency.USD.number
        840
        >>> Currency.UYN.number
        858
        """
        return _TABLE[self.name].number

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
    def withdrew_entities(self) -> Tuple[Historic, ...]:
        """
        Countries or other entities that do not use the currency anymore.
        :return: List of tuples of entities and dates when withdrawl happened.

        >>> Currency.UAK.withdrew_entities
        (Historic(entity='UKRAINE', name='Karbovanet', time=...),)
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

    @property
    def unit(self):
        """
        If the pint package is installed and currency units are defined by calling
        define_currency_units on any registry, this will return corresponding pint unit.

        >>> Currency.EUR.unit
        <Unit('EUR')>
        """
        return currency_unit(self.name)

    @property
    def subunit(self):
        """
        If the pint package is installed and currency units are defined by calling
        define_currency_units on any registry, this will return corresponding
        dummy pint subunit. These have non-standard currency codes, suffixed with 's'.

        >>> Currency.EUR.subunit
        <Unit('EURs')>
        """
        return currency_unit(self.name + "s")

    def __str__(self):
        return self.name

    _generate_enum(locals())
