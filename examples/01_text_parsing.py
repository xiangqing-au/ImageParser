"""Example 1 - text parsing helpers. Needs no phone and no OCR engine.

Run:  python examples/01_text_parsing.py
"""

from imageparser.naming import get_city_path
from imageparser.text_utils import search_google_info, search_price, to_float

# --- Google Maps summary text as OCR sees it -------------------------------
print(search_google_info("Fastest route 1hr 5 min (23.4 km) Light traffic"))   # (23.4, 65)

# --- Bolt fare text: two prices means "discounted price" is the second one --
BOLT_DISCOUNT = r"^(.*?)[\$S](\d+\.?\d+)(.*? .*?)[\$S](\d+\.?\d+)(.*?)$"
print(search_price("Bolt $25.10 fast $21.30 4 min", BOLT_DISCOUNT, 4))         # 21.3

print(to_float("$12.50"))                                                       # 12.5

# --- Existing screenshot naming --------------------------------------------
print(get_city_path("BOLT_NYC"))                                              # NYC
