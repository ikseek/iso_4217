from decimal import Decimal

from pint import UnitRegistry

from . import Currency


def define_currency_units(registry: UnitRegistry = None):
    """Define currency units in a given pint UnitRegistry"""
    registry = registry or UnitRegistry(non_int_type=Decimal)
    for currency in Currency:
        if currency.subunit_exp:
            alias = currency.unit.replace(" ", "_")
            subunits = 10 ** currency.subunit_exp
            registry.define("s{0} = [currency_{0}]".format(currency.name))
            registry.define(
                "{0} = s{0} * {1} = _ = {2} = {3}".format(
                    currency.name, subunits, alias, alias.lower()
                )
            )
        else:
            registry.define("s{0} = [currency_{0}] = _ = {0}".format(currency.name))
    return registry
