"""Static lookup tables shared across the package."""

from __future__ import annotations

from typing import Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Screenshot regions of interest
# --------------------------------------------------------------------------- #
#: ``profile -> scope -> (top, bottom, left, right)`` in screen pixels.
#: The default profile was tuned on a 720x1560 screen. Add your own profile
#: for other resolutions and reference it from ``config.yaml``.
SCREEN_PROFILES: Dict[str, Dict[str, Tuple[int, int, int, int]]] = {
    "hd720": {
        "B": (875, 1070, 500, 690),     # Bolt fare estimate
        "BI": (650, 1380, 40, 650),     # Bolt fare breakdown
        "D": (780, 980, 450, 710),      # DiDi selected fare
        "DI": (850, 1300, 20, 700),     # DiDi fare breakdown
        "UX": (1090, 1310, 400, 710),  # UberX selected fare
        "UX1": (820, 1010, 490, 710),  # UberX fare in the ride options list
        "UXI": (420, 1200, 20, 710),   # Uber fare breakdown
        "G": (1320, 1450, 10, 710),     # Google Maps route summary (compact)
        "G2": (1020, 1370, 10, 710),    # Google Maps route summary (expanded)
    },
}

#: Normalised fee name -> labels that may appear on the fare breakdown screen.
CHARGE_MAP: Dict[str, List[str]] = {
    "toll": ["Estimated Tolls", "Estimated tolls", "Highway Fee"],
    "surcharge": ["CTP Fee", "Airport Fee", "Estimated surcharges", "Holiday Surcharge"],
    "base": ["Base fare", "Start"],
    "rateB": ["Base Fare"],
    "kilo": ["per kilometre", "Per km"],
    "minute": ["Per Minute", "Per min"],
    "booking": ["Booking Fee", "Convenience Fee", "Booking fee"],
    "rateT": ["Time Rate"],
    "rateD": ["Distance Rate"],
    "minimum": ["Minimum fare", "Minimum Fare", "Minimum price"],
    "long": ["Above 20 km"],
    "short": ["0-12 km", "12 km", "0 - 12 km"],
    "medium": ["12 - 20 km", "20 km"],
}

#: Column order of the result CSV written by the analyser.
RESULT_FIELDS: List[str] = [
    "id", "date", "time", "dist", "trip", "toll", "surcharge", "surge", "price",
    "base", "minimum", "minute", "kilo", "booking",
    "rateB", "short", "medium", "long", "rateT", "rateD",
    "valid", "src", "dst",
]
