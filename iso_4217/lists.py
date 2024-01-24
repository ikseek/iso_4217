import locale
from datetime import datetime
from itertools import chain, groupby
from typing import (
    Callable,
    Dict,
    FrozenSet,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
)
from xml.etree import ElementTree


class ApproxDate(NamedTuple):
    """Parsed approximate currency withdrawal date"""

    year: int
    month: Optional[int] = None

    def __str__(self):
        year, month = self.year, self.month
        return "{}-{:02}".format(year, month) if month else str(year)

    @classmethod
    def from_str(cls, text: str):
        return cls(*(int(p) for p in text.split("-")))


class ApproxTimeSpan(NamedTuple):
    """Parsed approximate currency withdrawal time span"""

    end: ApproxDate
    begin: Optional[ApproxDate] = None

    def __str__(self):
        return "{} to {}".format(self.begin, self.end) if self.begin else str(self.end)

    @classmethod
    def from_str(cls, text: str):
        return cls(*(ApproxDate.from_str(date) for date in text.split(" to ")))


class Historic(NamedTuple):
    """
    Contains information about currency withdrawal event.
    """

    entity: str
    name: str
    time: ApproxTimeSpan


class CurrencyInfo(NamedTuple):
    """
    Contains all the information about currency joined from both lists
    """

    code: str
    name: str
    number: Optional[int]
    subunit_exp: Optional[int]
    is_fund: bool
    entities: FrozenSet[str]
    withdrew_entities: Tuple[Historic, ...]


def load() -> Tuple[datetime, dict]:
    current = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, "C")
    date1, active = _load_list("list-one.xml", "CcyTbl/CcyNtry", _currency_data)
    date2, historic = _load_list(
        "list-three.xml", "HstrcCcyTbl/HstrcCcyNtry", _historic_data
    )
    locale.setlocale(locale.LC_TIME, current)
    both = sorted(chain(active, historic), key=lambda c: c["code"])
    currencies = (
        _group_entities(list(g)) for _, g in groupby(both, lambda c: c["code"])
    )
    table = {c.code: c for c in currencies}
    return max(date1, date2), table


def _load_list(
    filename: str, path: str, convert: Callable[[ElementTree.Element], Optional[Dict]]
) -> Tuple[datetime, Iterable[Dict]]:
    tree = ElementTree.fromstring(_load_xml_resource(filename))
    date = datetime.strptime(tree.attrib["Pblshd"], "%Y-%m-%d")
    return date, filter(None, (convert(node) for node in tree.findall(path)))


def _load_xml_resource(filename: str) -> bytes:
    try:
        from importlib.resources import files

        return files().joinpath("data/" + filename).read_bytes()
    # Old python versions might miss
    # argument-less files function, files function itself or resources modules
    except (AttributeError, ImportError, TypeError):
        from pkg_resources import resource_string

        return resource_string(__name__, "data/" + filename)


def _currency_data(node: ElementTree.Element) -> Optional[Dict]:
    name = node.find("CcyNm")
    if name.text != "No universal currency":
        subunit_exp = node.find("CcyMnrUnts").text
        return dict(
            code=node.find("Ccy").text,
            number=int(node.find("CcyNbr").text),
            name=name.text.rstrip(),
            subunit_exp=int(subunit_exp) if subunit_exp != "N.A." else None,
            is_fund="IsFund" in name.attrib,
            entity=node.find("CtryNm").text.strip(),
        )


def _historic_data(node: ElementTree.Element) -> Dict:
    name = node.find("CcyNm")
    number = node.find("CcyNbr")
    return dict(
        code=node.find("Ccy").text,
        number=int(number.text) if number is not None else None,
        name=name.text.rstrip(),
        subunit_exp=None,
        is_fund="IsFund" in name.attrib,
        withdrew_entity=node.find("CtryNm").text.strip(),
        withdrawal_date=ApproxTimeSpan.from_str(node.find("WthdrwlDt").text),
    )


def _group_entities(entries: List[Dict]) -> CurrencyInfo:
    entities = frozenset(e["entity"] for e in entries if "entity" in e)
    withdrew_entities = (
        Historic(e["withdrew_entity"], e["name"], e["withdrawal_date"])
        for e in entries
        if "withdrew_entity" in e
    )
    withdrew_entities = tuple(sorted(withdrew_entities, key=lambda e: e.time))
    currency = entries[0]
    return CurrencyInfo(
        code=currency["code"],
        number=currency["number"],
        name=currency["name"],
        subunit_exp=currency["subunit_exp"],
        is_fund=currency["is_fund"],
        entities=entities,
        withdrew_entities=withdrew_entities,
    )
