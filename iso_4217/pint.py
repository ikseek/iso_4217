from decimal import Decimal
from typing import Union
from warnings import warn

from . import currency


class NoRegistry:
    def __init__(self, **kwargs):
        if kwargs:
            self._no_pint_installed()

    def _no_pint_installed(self):
        pass


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
            alias = c.value.replace(" ", "_")
            subunits = 10 ** c.subunit_exp
            registry.define("s{0} = [currency_{0}]".format(c.name))
            registry.define(
                "{0} = s{0} * {1} = _ = {2} = {3}".format(
                    c.name, subunits, alias, alias.lower()
                )
            )
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
