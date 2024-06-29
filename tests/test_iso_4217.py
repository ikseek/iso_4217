from iso_4217 import Currency, __version__
from iso_4217.lists import ApproxDate, ApproxTimeSpan


def test_version():
    assert __version__ == "0.6.240625"


def test_currency_count():
    assert len(Currency) == 305


def test_active_currencies_count():
    assert sum(bool(c.entities) for c in Currency) == 180


def test_uah():
    assert Currency.UAH.name == "UAH"
    assert Currency.UAH.value == "Hryvnia"
    assert Currency.UAH.number == 980
    assert Currency.UAH.entities == frozenset({"UKRAINE"})
    assert Currency.UAH.withdrew_entities == ()
    assert Currency.UAH.is_fund is False
    assert Currency.UAH.subunit_exp == 2


def test_eur():
    assert Currency.EUR.name == "EUR"
    assert Currency.EUR.value == "Euro"
    assert Currency.EUR.number == 978
    assert len(Currency.EUR.entities) == 36
    assert Currency.EUR.withdrew_entities == (
        ("SERBIA AND MONTENEGRO", "Euro", ApproxTimeSpan(ApproxDate(2006, 10))),
    )
    assert Currency.EUR.is_fund is False
    assert Currency.EUR.subunit_exp == 2


def test_ron():
    assert Currency.RON.name == "RON"
    assert Currency.RON.value == "Romanian Leu"
    assert Currency.RON.number == 946
    assert Currency.RON.entities == frozenset({"ROMANIA"})
    assert Currency.RON.withdrew_entities == (
        ("ROMANIA", "New Romanian Leu", ApproxTimeSpan(ApproxDate(2015, 6))),
    )
    assert Currency.RON.is_fund is False
    assert Currency.RON.subunit_exp == 2


def test_zwg():
    assert Currency.ZWG.name == "ZWG"
    assert Currency.ZWG.value == "Zimbabwe Gold"
    assert Currency.ZWG.number == 924
    assert Currency.ZWG.entities == frozenset({'ZIMBABWE'})


def test_bgk_bgj():
    assert Currency.BGK.value == "Lev A/62 (1989)"
    assert Currency.BGJ.value == "Lev A/52 (1989)"


def test_missing_codes():
    assert Currency.XFO.value == "Gold-Franc (2006)"
    assert Currency.XRE.value == "RINET Funds Code (1999)"
    assert Currency.XFU.value == "UIC-Franc (2013)"


def test_ves_ved():
    assert Currency.VES.number == 928
    assert Currency.VES.value == "Bolívar Soberano (VES)"
    assert Currency.VED.number == 926
    assert Currency.VED.value == "Bolívar Soberano (VED)"
