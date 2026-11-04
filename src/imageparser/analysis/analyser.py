"""Batch analysis: screenshots of a run -> one result CSV."""

from __future__ import annotations

import csv
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from ..constants import RESULT_FIELDS
from ..naming import screenshot_path
from ..routes import read_routes
from .parser import ScreenshotParser

logger = logging.getLogger(__name__)

FARE_GROUPS = (("B", "BI"), ("D", "DI"), ("UX", "UXI"))


def clean_address(address: str) -> str:
    """Lower-case an address and drop punctuation."""
    return re.sub(r"[^A-Za-z0-9 ]", "", str(address).lower())


class ScreenshotAnalyser:
    """Analyse every route of one run (one city, one date, one phone).

    Args:
        parser: Configured :class:`ScreenshotParser`.
        work_base: Workspace root containing ``routes/``.
        city: Route file name (``NYC`` for ``routes/NYC.csv``).
        date: Date label used in screenshot file names (e.g. ``0906``).
        screenshot_dir: Folder with the screenshots; the CSV is written here too.
        label: Name used in log messages (usually the phone alias).
    """

    def __init__(self, parser: ScreenshotParser, work_base: Path, city: str,
                 date: str, screenshot_dir: str, label: str = ""):
        self.parser = parser
        self.work_base = work_base
        self.city = city
        self.date = date
        self.dir = screenshot_dir
        self.label = label
        self.csv_path = os.path.join(screenshot_dir, f"ZZ_{city}_{date}.csv")

    def run(self) -> str:
        """Parse all routes and write the result CSV. Returns the CSV path."""
        logger.info("%s analyse routes start", self.label.upper())
        routes = read_routes(self.work_base, self.city)

        with open(self.csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=RESULT_FIELDS, extrasaction="ignore")
            writer.writeheader()
            groups = self._available_groups()
            for route_id, route in enumerate(routes, 1):
                for fare_id, info_id in groups:
                    row = self.analyse_route(route_id, route, fare_id, info_id)
                    writer.writerow(row)
                    if "time" in row:
                        print(f"{fare_id}:", row)

        logger.info("%s analyse finish, result: %s", self.label.upper(), self.csv_path)
        return self.csv_path

    def _available_groups(self) -> List[tuple[str, str]]:
        """Return the screenshot groups present in this run, preserving legacy output."""
        groups = []
        for fare_id, info_id in FARE_GROUPS:
            suffixes = (fare_id, info_id, "UX1") if fare_id == "UX" else (fare_id, info_id)
            if any(self._has_screenshot_suffix(suffix) for suffix in suffixes):
                groups.append((fare_id, info_id))
        return groups or [("B", "BI")]

    def _has_screenshot_suffix(self, suffix: str) -> bool:
        pattern = f"{self.city}{self.date}[0-9][0-9][0-9]{suffix}.png"
        return any(
            path
            for folder in (self.dir, os.path.join(self.dir, "dc"))
            for path in Path(folder).glob(pattern)
        )

    def analyse_route(self, route_id: int, route: Dict[str, object],
                      fare_id: str = "B", info_id: str = "BI") -> Dict[str, object]:
        """Parse one app's screenshots for a route into a result row."""
        row: Dict[str, object] = {
            "id": route_id, "src": clean_address(route["src"]),
            "dst": clean_address(route["dst"]), "surge": "", "valid": "",
        }
        fare_path = self._find_screenshot(route_id, fare_id)
        actual_fare_id = fare_id
        if fare_path is None and fare_id == "UX":
            fare_path = self._find_screenshot(route_id, "UX1")
            actual_fare_id = "UX1"
        if fare_path is not None:
            self.parser.parse(actual_fare_id, fare_path, row)

        info_path = self._find_screenshot(route_id, info_id)
        if info_path is not None:
            self.parser.parse(info_id, info_path, row)

        google_path = self._find_screenshot(route_id, "G")
        if google_path is None:
            google_path = self._find_alternative_google(route_id)
        if google_path is not None:
            self.parser.parse("G", google_path, row)
        return row

    def _find_screenshot(self, route_id: int, suffix: str) -> Optional[str]:
        """Prefer corrected screenshots and avoid stale Google images for corrected routes."""
        corrected = screenshot_path(os.path.join(self.dir, "dc"), self.city, self.date,
                                   route_id, suffix)
        primary = screenshot_path(self.dir, self.city, self.date, route_id, suffix)
        if os.path.exists(corrected):
            return corrected
        if suffix == "G" and self._has_correction_screenshots(route_id):
            return None
        return primary if os.path.exists(primary) else None

    def _has_correction_screenshots(self, route_id: int) -> bool:
        """Whether the correction folder contains any fare image for this route."""
        return any(
            os.path.exists(screenshot_path(os.path.join(self.dir, "dc"), self.city,
                                           self.date, route_id, suffix))
            for suffix in ("B", "BI", "D", "DI", "UX", "UX1", "UXI")
        )

    def _find_alternative_google(self, route_id: int) -> Optional[str]:
        """Find a G0/G1 image without renaming or modifying the input screenshot."""
        for i in range(2):
            alt = self._find_screenshot(route_id, f"G{i}")
            if alt is not None:
                return alt
        return None


def list_missing(directory: str, city: str, date: str, route_ids: List[int],
                 suffixes: List[str]) -> List[int]:
    """Return the route ids lacking at least one of the ``suffixes`` screenshots."""
    return [
        rid for rid in route_ids
        if not all(os.path.exists(screenshot_path(directory, city, date, rid, s)) for s in suffixes)
    ]
