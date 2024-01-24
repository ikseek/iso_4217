``iso_4217``: Yet another currency data package for Python
==========================================================
.. image:: https://github.com/ikseek/iso_4217/workflows/Python%20package/badge.svg
.. image:: https://img.shields.io/pypi/v/iso-4217?style=plastic
   :target: https://pypi.org/project/iso-4217/

This package contains ISO 4217 *active* and *historical* currency data.
Supports `pint`_ for operations with currency units.

>>> from iso_4217 import Currency
>>> Currency.USD
<Currency.USD: 'US Dollar'>
>>> Currency.USD.value
'US Dollar'
>>> Currency.USD.number
840
>>> Currency('US Dollar')
<Currency.USD: 'US Dollar'>
>>> Currency.JPY.entities
frozenset({'JAPAN'})
>>> Currency.ZWR
<Currency.ZWR: 'Zimbabwe Dollar (2009)'>
>>> Currency.ZWR.entities
frozenset()
>>> Currency.ZWR.withdrew_entities
(Historic(entity='ZIMBABWE', name='Zimbabwe Dollar'...2009, month=6), begin=None)),)
>>> Currency.VED
<Currency.VED: 'Bolívar Soberano (VED)'>


Pint units and subunits are available with convenient :code:`unit` and :code:`subunit`
properties on Currency. Accessing these properties requires `pint` package installed
and automatically defines currency units in application default registry.

>>> Currency.USD.unit * 5 + Currency.USD.subunit * 5
<Quantity(5.05, 'USD')>

Currency units can be defined in any UnitRegistry manually

>>> import pint
>>> from decimal import Decimal
>>> from iso_4217 import define_currency_units
>>> reg = define_currency_units(pint.UnitRegistry(non_int_type=Decimal))
>>> 5 * reg.USD
<Quantity(5, 'USD')>

But units from separate registries should not be mixed

>>> Currency.USD.unit == reg.USD
Traceback (most recent call last):
...
ValueError: Cannot operate with Unit and Unit of different registries.

If you want to replace registry used by Currency just replace the application registry:

>>> pint.set_application_registry(reg)
>>> Currency.USD.unit == reg.USD
True

Subunits are defined with `s` suffix:

>>> 5 * reg.USDs
<Quantity(5, 'USDs')>
>>> (5 * reg.USDs).to("USD")
<Quantity(0.05, 'USD')>
>>> (5 * reg.BHDs).to_base_units()
<Quantity(0.005, 'BHD')>

Each currency is defined within it's own dimension:

>>> (5 * reg.USD).to('EUR')
Traceback (most recent call last):
...
pint.errors.DimensionalityError: Cannot convert from 'USD' ([currency_USD]) to 'EUR' ([currency_EUR])

But automatic currency conversion can be made via pint Contexts

>>> context = pint.Context()
>>> eur_to_usd = lambda r, eur: eur * r("1.2 USD/EUR")
>>> context.add_transformation("[currency_EUR]", "[currency_USD]", eur_to_usd)
>>> (Currency.EUR.unit * 5).to('USD', context)
<Quantity(6.0, 'USD')>

Inspired by `iso4217`_ package by Hong Minhee.

.. _iso4217: https://github.com/dahlia/iso4217
.. _pint: https://pint.readthedocs.io
