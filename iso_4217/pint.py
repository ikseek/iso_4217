from pint import get_application_registry

from . import Currency


def define_currency_units(registry=None):
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
