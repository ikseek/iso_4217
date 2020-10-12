from datetime import datetime
from itertools import chain, groupby
from typing import Callable, Iterable, Optional, Tuple, Union
from xml.etree import ElementTree

from pkg_resources import resource_string


def load_lists() -> Tuple[datetime, dict]:
    # Used to keep track and separate (historical) currencies sharing the same
    # currency number. Pre-initialized with None to avoid having None assigned
    # as enum value to number-less historical funds.
    seen_codes = {None: {None: 0}}
    date1, active = _load_list(
        "list_one.xml", "CcyTbl/CcyNtry", _currency_data, seen_codes
    )
    date2, historical = _load_list(
        "list_three.xml", "HstrcCcyTbl/HstrcCcyNtry", _historic_data, seen_codes
    )
    both = sorted(
        chain(active, historical),
        key=lambda c: (c["currency"], c["entity"]),
    )
    currencies = (
        _group_entities(list(g)) for _, g in groupby(both, lambda c: c["currency"])
    )
    return max(date1, date2), {c.pop("currency"): c for c in currencies}


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


def _currency_data(node: ElementTree, seen_codes: dict) -> Optional[dict]:
    name = node.find("CcyNm")
    if name.text != "No universal currency":
        units = node.find("CcyMnrUnts").text
        currency = node.find("Ccy").text
        return dict(
            entity=node.find("CtryNm").text.strip(),
            name=name.text,
            currency=currency,
            number=_currency_number(seen_codes, currency, node.find("CcyNbr").text),
            is_fund="IsFund" in name.attrib,
            units=int(units) if units != "N.A." else None,
            historic=False,
        )


def _historic_data(node: ElementTree, seen_codes: dict) -> dict:
    def field(tag_name):
        sub_node = node.find(tag_name)
        return sub_node.text if sub_node is not None else None

    name = node.find("CcyNm")
    currency = field("Ccy")
    return dict(
        entity=field("CtryNm").strip(),
        name=name.text,
        currency=currency,
        number=_currency_number(seen_codes, currency, field("CcyNbr")),
        withdrawl_date=field("WthdrwlDt"),
        is_fund="IsFund" in name.attrib,
        units=None,
        historic=True,
    )


def _currency_number(
    seen_codes: dict, currency: str, number: Optional[str]
) -> Union[int, Tuple[int, int]]:
    number = int(number) if number else None
    code_currencies = seen_codes.setdefault(number, {})
    currency_unique_code = code_currencies.setdefault(currency, len(code_currencies))
    return (number, currency_unique_code) if currency_unique_code else number


def _group_entities(currencies) -> dict:
    entities = frozenset(c.pop("entity") for c in currencies if not c["historic"])
    withdrawn_entities = tuple(
        (c.pop("entity"), c.pop("withdrawl_date")) for c in currencies if c["historic"]
    )
    currencies[0].pop("historic")
    currencies[0]["entities"] = entities
    currencies[0]["withdrawn_entities"] = withdrawn_entities
    return currencies[0]
