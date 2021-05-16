from . import currency

try:
    from pint import UndefinedUnitError, get_application_registry
except ImportError:

    def get_application_registry():
        raise RuntimeError("Units support requires pint package installed.")


def define_currency_units(registry):
    """Define currency units in a given pint UnitRegistry"""
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
    return registry


def currency_unit(name: str):
    registry = get_application_registry()
    try:
        return registry.Unit(name)
    except UndefinedUnitError:
        return define_currency_units(registry).Unit(name)
