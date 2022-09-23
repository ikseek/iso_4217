from urllib.request import urlopen

import pytest

from iso_4217.lists import _load_xml_resource


@pytest.mark.parametrize("list_xml", ("list-one.xml", "list-three.xml"))
def test_data_tables_are_up_to_date(list_xml):
    LISTS_URL = (
        "https://www.six-group.com/dam/download/financial-information/"
        "data-center/iso-currrency/lists/"
    )
    assert _load_xml_resource(list_xml) == urlopen(LISTS_URL + list_xml).read()
