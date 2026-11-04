import pytest

from imageparser.naming import (
    get_city_path,
)
from imageparser.text_utils import (
    search_google_info, search_google_small, search_price, to_float, to_int,
)

BOLT_DISCOUNT = r"^(.*?)[\$S](\d+\.?\d+)(.*? .*?)[\$S](\d+\.?\d+)(.*?)$"


def test_to_float_and_int():
    assert to_float("$12.50") == 12.5
    assert to_float("n/a") == 0.0
    assert to_int("20 km") == 20


def test_google_info_with_hours():
    assert search_google_info("Fastest 1hr 5 min (23.4 km) traffic") == (23.4, 65)


def test_google_info_no_match():
    assert search_google_info("nothing here") == (0.0, 0)


def test_google_small_fallback():
    assert search_google_small("12 min away 5.2 km") == (5.2, 12)


def test_search_price_discount_group():
    assert search_price("Bolt $25.10 fast $21.30 4 min", BOLT_DISCOUNT, 4) == 21.3


def test_search_price_missing_decimal_point():
    assert search_price("x $2130 y z", r"^(.*?)[\$S](\d+)(.*? .*?)$", 2) == 21.3


@pytest.mark.parametrize("name,city", [
    ("BOLT_NYC", "NYC"),
    ("INDRIVE_HOU", "HOU"),
    ("GOOGLE_LAX", "LAX"),
    ("NYC", "NYC"),
])
def test_city_path(name, city):
    assert get_city_path(name) == city
