from datetime import datetime
from itertools import chain, groupby
from typing import Callable, FrozenSet, Iterable, NamedTuple, Optional, Tuple
from xml.etree import ElementTree

from pkg_resources import resource_string


class ApproxDate(NamedTuple):
    year: int
    month: Optional[int] = None

    def __str__(self):
        return "{}-{}".format(self.year, self.month) if self.month else str(self.year)

    @classmethod
    def from_str(cls, text: str):
        return cls(*(int(p) for p in text.split("-")))


class ApproxTimeSpan(NamedTuple):
    end: ApproxDate
    begin: Optional[ApproxDate] = None

    def __str__(self):
        return "{} to {}".format(self.begin, self.end) if self.begin else str(self.end)

    @classmethod
    def from_str(cls, text: str):
        return cls(*(ApproxDate.from_str(date) for date in text.split(" to ")))


class Historic(NamedTuple):
    """Datatype that sets apart active and historic currencies"""

    value: Optional[int]
    code: str


class CurrencyInfo(NamedTuple):
    """
    Contains all the information about currency joined from both lists
    """

    code: str
    number: Optional[int]
    unit: str
    subunit_exp: Optional[int]
    is_fund: bool
    entities: FrozenSet[str]
    withdrew_entities: Tuple[Tuple[str, ApproxTimeSpan], ...]

    @property
    def discriminator(self):
        return self.number if self.entities else Historic(self.number, self.code)


def load() -> Tuple[datetime, dict]:
    # Used to keep track and separate (historical) currencies sharing the same
    # currency number. Pre-initialized with None to avoid having None assigned
    # as enum value to number-less historical funds.
    date1, active = _load_list("list_one.xml", "CcyTbl/CcyNtry", _currency_data)
    date2, historical = _load_list(
        "list_three.xml", "HstrcCcyTbl/HstrcCcyNtry", _historic_data
    )
    both = sorted(
        chain(active, historical),
        key=lambda c: (c["code"], c["entity"]),
    )
    currencies = (
        _group_entities(list(g)) for _, g in groupby(both, lambda c: c["code"])
    )
    table = ((c["code"], CurrencyInfo(**c)) for c in currencies)
    return max(date1, date2), {code: info for code, info in table}


def _load_list(
    filename: str, path: str, convert: Callable
) -> Tuple[datetime, Iterable[dict]]:
    tree = ElementTree.fromstring(_load_xml_resource(filename))
    date = datetime.strptime(tree.attrib["Pblshd"], "%Y-%m-%d")
    return date, filter(None, (convert(node) for node in tree.findall(path)))


def _load_xml_resource(filename: str) -> str:
    return resource_string(__name__, "data/" + filename)


def _currency_data(node: ElementTree) -> Optional[dict]:
    unit = node.find("CcyNm")
    if unit.text != "No universal currency":
        subunit_exp = node.find("CcyMnrUnts").text
        code = node.find("Ccy").text
        return dict(
            code=code,
            number=int(node.find("CcyNbr").text),
            unit=unit.text.rstrip(),
            subunit_exp=int(subunit_exp) if subunit_exp != "N.A." else None,
            is_fund="IsFund" in unit.attrib,
            entity=node.find("CtryNm").text.strip(),
        )


def _historic_data(node: ElementTree) -> dict:
    def field(tag_name):
        sub_node = node.find(tag_name)
        return sub_node.text if sub_node is not None else None

    unit = node.find("CcyNm")
    code = field("Ccy")
    return dict(
        code=code,
        number=int(field("CcyNbr")) if field("CcyNbr") else None,
        unit=unit.text.rstrip(),
        subunit_exp=None,
        is_fund="IsFund" in unit.attrib,
        entity=field("CtryNm").strip(),
        withdrawal_date=ApproxTimeSpan.from_str(node.find("WthdrwlDt").text),
    )


def _group_entities(currencies) -> dict:
    entities = frozenset(
        c.pop("entity") for c in currencies if "withdrawal_date" not in c
    )
    withdrew_entities = (
        (c.pop("entity"), c.pop("withdrawal_date"))
        for c in currencies
        if "withdrawal_date" in c
    )
    withdrew_entities = tuple(sorted(withdrew_entities, key=lambda e: e[1]))

    currencies[0]["entities"] = entities
    currencies[0]["withdrew_entities"] = withdrew_entities
    return currencies[0]
