from pint import UnitRegistry, get_application_registry

from . import Currency


def define_currency_units(registry: UnitRegistry = None):
    """Define currency units in a given pint UnitRegistry"""
    registry = registry or get_application_registry()
    for currency in Currency:
        if currency.subunit_exp:
            alias = currency.unit.replace(" ", "_")
            subunits = 10 ** currency.subunit_exp
            registry.define(
                "{0} = [currency_{0}] = _ = {1}".format(currency.name, alias)
            )
            registry.define("{0}_su = {0} / {1}".format(currency.name, subunits))
        else:
            registry.define("{0} = [currency_{0}] = _ = {0}_su".format(currency.name))
    return registry
