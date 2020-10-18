from datetime import datetime
from itertools import chain, groupby
from typing import Callable, FrozenSet, Iterable, NamedTuple, Optional, Tuple, Union
from xml.etree import ElementTree

from pkg_resources import resource_string


class CurrencyInfo(NamedTuple):
    """
    Contains all the information about currency joined from both lists
    """

    number: Optional[int]
    """Currency numeric code, non-unique"""
    discriminator: int
    unit: str
    subunit_exp: Optional[int]
    is_fund: bool
    entities: FrozenSet[str]
    withdrew_entities: Tuple[Tuple[str, str], ...]


def load() -> Tuple[datetime, dict]:
    # Used to keep track and separate (historical) currencies sharing the same
    # currency number. Pre-initialized with None to avoid having None assigned
    # as enum value to number-less historical funds.
    seen_numbers = {None: {None: 0}}
    date1, active = _load_list(
        "list_one.xml", "CcyTbl/CcyNtry", _currency_data, seen_numbers
    )
    date2, historical = _load_list(
        "list_three.xml", "HstrcCcyTbl/HstrcCcyNtry", _historic_data, seen_numbers
    )
    both = sorted(
        chain(active, historical),
        key=lambda c: (c["code"], c["entity"]),
    )
    currencies = (
        _group_entities(list(g)) for _, g in groupby(both, lambda c: c["code"])
    )
    table = ((c.pop("code"), CurrencyInfo(**c)) for c in currencies)
    return max(date1, date2), {code: info for code, info in table}


def _load_list(
    filename: str, path: str, convert: Callable, seen_codes: dict
) -> Tuple[datetime, Iterable[dict]]:
    tree = ElementTree.fromstring(_load_xml_resource(filename))
    date = datetime.strptime(tree.attrib["Pblshd"], "%Y-%m-%d")
    return date, filter(
        None, (convert(node, seen_codes) for node in tree.findall(path))
    )


def _load_xml_resource(filename: str) -> str:
    return resource_string(__name__, "data/" + filename)


def _currency_data(node: ElementTree, seen_numbers: dict) -> Optional[dict]:
    unit = node.find("CcyNm")
    if unit.text != "No universal currency":
        subunit_exp = node.find("CcyMnrUnts").text
        code = node.find("Ccy").text
        number, disc = _currency_number(seen_numbers, code, node.find("CcyNbr").text)
        return dict(
            code=code,
            number=number,
            discriminator=disc,
            unit=unit.text,
            subunit_exp=int(subunit_exp) if subunit_exp != "N.A." else None,
            is_fund="IsFund" in unit.attrib,
            entity=node.find("CtryNm").text.strip(),
            historic=False,
        )


def _historic_data(node: ElementTree, seen_numbers: dict) -> dict:
    def field(tag_name):
        sub_node = node.find(tag_name)
        return sub_node.text if sub_node is not None else None

    unit = node.find("CcyNm")
    code = field("Ccy")
    number, disc = _currency_number(seen_numbers, code, field("CcyNbr"))
    return dict(
        code=code,
        number=number,
        discriminator=disc,
        unit=unit.text,
        subunit_exp=None,
        is_fund="IsFund" in unit.attrib,
        entity=field("CtryNm").strip(),
        withdrawal_date=field("WthdrwlDt"),
        historic=True,
    )


def _currency_number(
    seen_numbers: dict, code: str, number: Optional[str]
) -> Union[int, Tuple[int, int]]:
    number = int(number) if number else None
    codes = seen_numbers.setdefault(number, {})
    discriminator = codes.setdefault(code, len(codes))
    return number, discriminator


def _group_entities(currencies) -> dict:
    entities = frozenset(c.pop("entity") for c in currencies if not c["historic"])
    withdrew_entities = tuple(
        (c.pop("entity"), c.pop("withdrawal_date")) for c in currencies if c["historic"]
    )
    currencies[0].pop("historic")
    currencies[0]["entities"] = entities
    currencies[0]["withdrew_entities"] = withdrew_entities
    return currencies[0]
