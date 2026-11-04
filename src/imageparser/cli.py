"""Command line interface for screenshot analysis and reports.

Analyse existing screenshots::

    imageparser --phone phone_a --city NYC --date 0906 --analyse

Report (no phone or config needed)::

    imageparser --report workspace/screenshots/0906_NYC_phone_a/ZZ_NYC_0906.csv
    imageparser --report run_a/ZZ_NYC_0906.csv run_b/ZZ_NYC_0906.csv -o compare.html
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import date as _date
from pathlib import Path
from typing import List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "imageparser"

from .config import load_config
from .naming import get_city_path

#: Arguments required for analysis (but not for --report).
ANALYSIS_ARGUMENTS = ("phone", "city", "date")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="imageparser",
        description="Analyse existing fare screenshots and build reports.")
    parser.add_argument(
        "--config",
        help="YAML config path (default: IMAGEPARSER_CONFIG, ./config.yaml, then config.example.yaml)",
    )
    parser.add_argument("--phone", help="phone alias (screen profile) defined in config.yaml")
    parser.add_argument("--city",
                        help="city or legacy task name, e.g. NYC or BOLT_NYC")
    parser.add_argument("--date",
                        help="date label for file names, e.g. 0906 (MMDD); 0000 = today")
    parser.add_argument("--analyse", action="store_true",
                        help="analyse existing screenshots (analysis is the only run mode)")
    parser.add_argument("--report", nargs="+", metavar="CSV",
                        help="build an HTML report from one or more result CSVs and exit")
    parser.add_argument("-o", "--output", metavar="PATH",
                        help="output path for --report (default: report_<csv stem>.html next to the CSV)")
    return parser


def _missing_analysis_arguments(args: argparse.Namespace) -> List[str]:
    return [name for name in ANALYSIS_ARGUMENTS if getattr(args, name) is None]


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Report mode: no phone, config or route range involved
    if args.report:
        from .report import write_report

        out = write_report([Path(p) for p in args.report], args.output)
        print(f"Report written to {out}")
        return

    missing = _missing_analysis_arguments(args)
    if missing or not args.analyse:
        if not args.analyse:
            missing.append("analyse")
        parser.error("the following arguments are required unless --report is used: "
                     + ", ".join(f"--{name}" for name in missing))

    config = load_config(args.config)
    today = _date.today()
    date_label = f"{today.month:02d}{today.day:02d}" if args.date == "0000" else args.date
    phone = args.phone.lower()
    city = get_city_path(args.city.upper())
    profile = config.phone(phone).profile
    screenshot_dir = config.work_base / "screenshots" / f"{date_label}_{city}_{phone}"
    os.makedirs(screenshot_dir, exist_ok=True)

    from .analysis import ScreenshotAnalyser, ScreenshotParser, create_engine

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s")
    engine = create_engine(config.ocr_engine, config.ocr_gpu, config.tesseract_cmd)
    parser_instance = ScreenshotParser(engine, profile)
    csv_path = ScreenshotAnalyser(
        parser_instance, config.work_base, city, date_label, str(screenshot_dir), phone,
    ).run()
    print(f"Finish analysing {date_label} {phone} {city}. Result: {csv_path}")


if __name__ == "__main__":
    main()
