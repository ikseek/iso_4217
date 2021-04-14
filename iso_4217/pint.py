from decimal import Decimal
from typing import Union
from warnings import warn

from . import currency


class NoRegistry:
    def __init__(self, **kwargs):
        if kwargs:
            NoRegistry._needs_pint()

    class Unit:
        def __init__(self, _):
            NoRegistry._needs_pint()

    @staticmethod
    def _needs_pint():
        raise RuntimeError(
            "This feature requires pint package installed. "
            "After that currencies should be defined in a registry by {} call".format(
                define_currency_units.__name__
            )
        )


try:
    from pint import UnitRegistry
except ImportError:
    UnitRegistry = NoRegistry

currency_registry: Union[NoRegistry, UnitRegistry] = NoRegistry()


def define_currency_units(registry: UnitRegistry = None):
    """Define currency units in a given pint UnitRegistry"""
    registry = registry or UnitRegistry(non_int_type=Decimal)
    for c in currency.Currency:
        if c.subunit_exp is None:
            registry.define("{0} = [currency_{0}]".format(c.name))
        else:
            alias1 = c.value.replace(" ", "_")
            alias2 = alias1.lower()
            registry.define(
                "{0} = [currency_{0}] = _ = {1} = {2}".format(c.name, alias1, alias2)
            )
            registry.define("{0}s = {0} / {1}".format(c.name, 10 ** c.subunit_exp))
    _keep_currency_registry(registry)
    return registry


def _keep_currency_registry(registry: UnitRegistry):
    global currency_registry
    currency_registry, prev_registry = registry, currency_registry
    if prev_registry is not None:
        warn(
            "Currency units were registered in more than one UnitRegistry. "
            "Only the last one will be used by Currency enum to cast to units."
        )
