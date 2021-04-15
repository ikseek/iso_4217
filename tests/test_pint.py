from decimal import Decimal

import pint
import pytest

from iso_4217 import define_currency_units


@pytest.fixture(scope="module")
def reg():
    reg = pint.UnitRegistry(non_int_type=Decimal)
    return define_currency_units(reg)


def test_hryvnias(reg):
    assert reg("5 Hryvnias") == 5 * reg.UAH


def test_us_dollars(reg):
    assert reg("5 US_Dollar") == 5 * reg.USD


def test_us_dollar_cents(reg):
    assert 5 * reg.USDs == Decimal("0.05") * reg.USD


def test_cant_convert_dollars_euro(reg):
    with pytest.raises(pint.DimensionalityError):
        (reg.USD * 5).to("EUR")


def test_convert_with_context_dollars_euro(reg):
    c = pint.Context()
    c.add_transformation(
        "[currency_USD]", "[currency_EUR]", lambda r, u: 1.2 * r.EUR / r.USD * u
    )
    dollars = 5 * reg.USD
    euros = 6 * reg.EUR

    assert dollars.to("EUR", c) == euros
