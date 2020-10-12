``iso_4217``: Yet another currency data package for Python
==========================================================
.. image:: https://travis-ci.org/ikseek/iso_4217.svg?branch=main

This package contains ISO 4217 active and historical currency data.
Written and tested for Python 3.6 and above.

>>> from iso_4217 import Currency
>>> Currency.USD
<Currency.USD: 840>
>>> Currency.USD.full_name
'US Dollar'
>>> Currency(840)
<Currency.USD: 840>
>>> Currency.JPY.entities
frozenset({'JAPAN'})
>>> Currency.ZWR
<Currency.ZWR: 935>
>>> Currency.ZWR.entities
frozenset()
>>> Currency.ZWR.withdrawn_entities
(('ZIMBABWE', '2009-06'),)

Inspired by `iso4217`_ package by Hong Minhee.

.. _iso4217: https://github.com/dahlia/iso4217
