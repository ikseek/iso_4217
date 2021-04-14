``iso_4217``: Yet another currency data package for Python
==========================================================
.. image:: https://github.com/ikseek/iso_4217/workflows/Python%20package/badge.svg
.. image:: https://img.shields.io/pypi/v/iso-4217?style=plastic
   :target: https://pypi.org/project/iso-4217/

This package contains ISO 4217 active and historical currency data.
Written and tested for Python 3.6 and above.

>>> from iso_4217 import Currency
>>> Currency.USD
<Currency.USD: 'US Dollar'>
>>> Currency.USD.value
'US Dollar'
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

Can define units in pint UnitRegistry:

>>> from iso_4217.pint import define_currency_units
>>> reg = define_currency_units()
>>> 5 * reg.USD
<Quantity(5, 'USD')>
>>> reg("5 Euros")
<Quantity(5, 'EUR')>

Subunits are defined with `s` prefix:

>>> 5 * reg.sUSD
<Quantity(5, 'sUSD')>
>>> (5 * reg.sUSD).to("USD")
<Quantity(0.05, 'USD')>
>>> (5 * reg.sBHD).to_base_units()
<Quantity(0.005, 'BHD')>

Each currency is defined within it's own dimension:

>>> (5 * reg.USD).to('EUR')
Traceback (most recent call last):
...
pint.errors.DimensionalityError: Cannot convert from 'USD' ([currency_USD]) to 'EUR' ([currency_EUR])

Pint units and subunits are also available with convenient `unit` and `subunit`
properties on Currency

>>> Currency.USD.unit * 5 + Currency.USD.subunit * 5
<Quantity(5.05, 'USD')>

Inspired by `iso4217`_ package by Hong Minhee.

.. _iso4217: https://github.com/dahlia/iso4217
