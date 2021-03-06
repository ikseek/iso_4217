from iso_4217 import Currency, __version__


def test_version():
    assert __version__ == "0.2.180829"


def test_currency_count():
    assert len(Currency) == 302


def test_active_currencies_count():
    assert sum(bool(c.entities) for c in Currency) == 179


def test_uah():
    assert Currency.UAH.value == 980
    assert Currency.UAH.name == "UAH"
    assert Currency.UAH.unit == "Hryvnia"
    assert Currency.UAH.entities == frozenset({"UKRAINE"})
    assert Currency.UAH.withdrew_entities == ()
    assert Currency.UAH.is_fund is False
    assert Currency.UAH.subunit_exp == 2


def test_eur():
    assert Currency.EUR.value == 978
    assert Currency.EUR.name == "EUR"
    assert Currency.EUR.unit == "Euro"
    assert len(Currency.EUR.entities) == 35
    assert Currency.EUR.withdrew_entities == (("SERBIA AND MONTENEGRO", "2006-10"),)
    assert Currency.EUR.is_fund is False
    assert Currency.EUR.subunit_exp == 2


def test_ron():
    assert Currency.RON.value == 946
    assert Currency.RON.name == "RON"
    assert Currency.RON.unit == "Romanian Leu"
    assert Currency.RON.entities == frozenset({"ROMANIA"})
    assert Currency.RON.withdrew_entities == (("ROMANIA", "2015-06"),)
    assert Currency.RON.is_fund is False
    assert Currency.RON.subunit_exp == 2


def test_missing_codes():
    assert Currency.XFO.value == (None, 1)
    assert Currency.XRE.value == (None, 2)
    assert Currency.XFU.value == (None, 3)
