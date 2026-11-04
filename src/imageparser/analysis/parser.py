"""Turn one screenshot into structured fields of a result row."""

from __future__ import annotations

import logging
import os
import re
import time
from typing import Dict, List

import cv2
import numpy as np

from ..constants import CHARGE_MAP, SCREEN_PROFILES
from ..text_utils import (
    search_google_info, search_google_small, search_price, to_float,
)
from .engines import OcrEngine

logger = logging.getLogger(__name__)

Row = Dict[str, object]

_RANGE_VALUE = re.compile(r"^\D*(\d+(?:\.\d+)?-\d+(?:\.\d+)?)\D*$")
_LIST_PRICE = re.compile(r"(?<!\d)(\d+(?:[.-]\d{2})|\d{3,4})(?!\d)")
_BOLT_PRICE = r"^(.*?)[\$S](\d+\.?\d+)(.*? .*?)$"
_BOLT_DISCOUNT = r"^(.*?)[\$S](\d+\.?\d+)(.*? .*?)[\$S](\d+\.?\d+)(.*?)$"


class ScreenshotParser:
    """Extract values from a screenshot into ``row`` (modified in place).

    Screenshot types (``file_id``):

    * ``B``  - Bolt ride options: fare estimate
    * ``BI`` - Bolt fare breakdown: fee items
    * ``D`` / ``DI`` - DiDi selected fare and fare breakdown
    * ``UX`` / ``UX1`` / ``UXI`` - UberX fare and fare breakdown
    * ``G``  - Google Maps: distance and duration
    """

    def __init__(self, engine: OcrEngine, profile: str = "hd720"):
        if profile not in SCREEN_PROFILES:
            raise KeyError(f"Unknown screen profile '{profile}'. Known: {', '.join(SCREEN_PROFILES)}")
        self.engine = engine
        self.regions = SCREEN_PROFILES[profile]

    # ------------------------------------------------------------------ #
    # public API
    # ------------------------------------------------------------------ #
    def parse(self, file_id: str, path: str, row: Row) -> None:
        """Dispatch on ``file_id`` and fill ``row``."""
        image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

        if file_id in ("B", "D", "UX", "UX1"):
            taken = time.localtime(os.path.getmtime(path))
            row["date"] = time.strftime("%Y/%m/%d", taken)
            row["time"] = time.strftime("%H:%M", taken)
            self.parse_fare(image, row, file_id)
        elif file_id.endswith("I"):
            self.parse_info(image, file_id, row)
        elif file_id.startswith("G"):
            self.parse_google(image, row)

    # ------------------------------------------------------------------ #
    # per screen type
    # ------------------------------------------------------------------ #
    def parse_fare(self, image: np.ndarray, row: Row, scope: str = "B") -> None:
        text = self._text(image, scope)
        if scope == "B":
            self._save_price(text, row)
        else:
            self._save_list_price(text, row)

    def parse_info(self, image: np.ndarray, scope: str, row: Row) -> None:
        self._save_detail(self._lines(image, scope), row)

    def parse_google(self, image: np.ndarray, row: Row) -> None:
        """Read distance/duration, trying progressively looser patterns."""
        texts = [self._text(image, "G"), self._text(image, "G2")]
        for parse in (search_google_info, search_google_small):
            for text in texts:
                distance, duration = parse(text)
                if distance and duration:
                    row["dist"], row["trip"] = distance, duration
                    return
        row["dist"], row["trip"] = 0.0, 0

    # ------------------------------------------------------------------ #
    # OCR plumbing
    # ------------------------------------------------------------------ #
    def _crop(self, image: np.ndarray, scope: str) -> np.ndarray:
        top, bottom, left, right = self.regions[scope]
        return image[top:bottom, left:right]

    def _text(self, image: np.ndarray, scope: str) -> str:
        try:
            return self.engine.read_text(self._crop(image, scope))
        except Exception:  # noqa: BLE001 - a bad crop must not abort the whole analysis
            logger.exception("OCR failed for scope %s", scope)
            return ""

    def _lines(self, image: np.ndarray, scope: str) -> List[str]:
        return self.engine.read_lines(self._crop(image, scope))

    # ------------------------------------------------------------------ #
    # result extraction
    # ------------------------------------------------------------------ #
    @staticmethod
    def _save_price(text: str, row: Row) -> None:
        """Pick the price from Bolt fare text (the discounted price if two are shown)."""
        if len(text.split()) == 1:
            row["price"] = search_price(text, _BOLT_PRICE, 2)
            return
        row["price"] = search_price(text, _BOLT_DISCOUNT, 4)
        if row["price"] == 0.0:
            row["price"] = search_price(text, _BOLT_PRICE, 2)

    @staticmethod
    def _save_list_price(text: str, row: Row) -> None:
        """Pick the original fare shown after a discounted fare in app ride lists."""
        prices = _LIST_PRICE.findall(text)
        if not prices:
            return
        value = prices[-1].replace("-", ".")
        if "." not in value and len(value) > 2:
            value = f"{value[:-2]}.{value[-2:]}"
        row["price"] = to_float(value)

    @staticmethod
    def _save_detail(lines: List[str], row: Row) -> None:
        """Map fare labels and values onto result columns."""
        for item, labels in CHARGE_MAP.items():
            fee, range_value, found = 0.0, None, False
            for label in labels:
                for index, line in enumerate(lines):
                    if label not in line:
                        continue
                    found = True
                    value = line.split(label, 1)[1].strip()
                    if not value and index + 1 < len(lines):
                        value = lines[index + 1]
                    range_match = _RANGE_VALUE.match(value)
                    if range_match:              # e.g. "0-12" km bracket
                        range_value = range_match.group(1)
                    else:
                        fee += to_float(value)

            if range_value is not None:
                row[item] = range_value
            elif fee != 0.0:
                row[item] = fee
            elif found:
                row[item] = 0
