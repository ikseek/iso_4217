``iso_4217``: Yet another currency data package for Python
==========================================================
.. image:: https://github.com/ikseek/iso_4217/workflows/Python%20package/badge.svg
.. image:: https://img.shields.io/pypi/v/iso-4217?style=plastic
   :target: https://pypi.org/project/iso-4217/

This package contains ISO 4217 active and historical currency data.
Written and tested for Python 3.6 and above.

>>> from iso_4217 import Currency
>>> Currency.USD
<Currency.USD: 840>
>>> Currency.USD.unit
'US Dollar'
>>> Currency(840)
<Currency.USD: 840>
>>> Currency.JPY.entities
frozenset({'JAPAN'})
>>> Currency.ZWR
<Currency.ZWR: Historic(number=935, code='ZWR')>
>>> Currency.ZWR.entities
frozenset()
>>> Currency.ZWR.withdrew_entities
(('ZIMBABWE', ApproxTimeSpan(end=ApproxDate(year=2009, month=6), begin=None)),)

Can define units in pint UnitRegistry:

>>> from pint import UnitRegistry
>>> from iso_4217.pint import define_currency_units
>>> reg = define_currency_units(UnitRegistry())
>>> 5 * reg.USD
<Quantity(5, 'USD')>
>>> reg("5 Euros")
<Quantity(5, 'EUR')>

Subunits are defined with _su suffix:

>>> 5 * reg.USD_su
<Quantity(5, 'USD_su')>
>>> (5 * reg.USD_su).to("USD")
<Quantity(0.05, 'USD')>

Each currency is defined within it's own dimension:

>>> (5 * reg.USD).to('EUR')
Traceback (most recent call last):
...
pint.errors.DimensionalityError: Cannot convert from 'USD' ([currency_USD]) to 'EUR' ([currency_EUR])

Inspired by `iso4217`_ package by Hong Minhee.

.. _iso4217: https://github.com/dahlia/iso4217
