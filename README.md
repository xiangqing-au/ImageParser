# ImageParser

ImageParser analyses existing fare screenshots with OCR and can render reports
from result CSVs. It does not connect to Android devices or capture images.

## Install

Use Python 3.9 or later and install one OCR extra:

```sh
python -m pip install -e ".[tesseract]"
```

Tesseract itself must also be installed and available on `PATH`. EasyOCR and
PaddleOCR are available through the `easyocr` and `paddle` extras.

## Analyse screenshots

The CLI loads configuration in this order: `--config`, the
`IMAGEPARSER_CONFIG` environment variable (or legacy `APPAUTOMATION_CONFIG`),
`config.yaml` in the current directory, then this repository's
`config.example.yaml`. Copy the example to `config.yaml` when you need local
settings.

Routes belong in `<work_base>/routes/<CITY>.csv` with `id,src,dst` columns.
Screenshots belong in
`<work_base>/screenshots/<DATE>_<CITY>_<PHONE>/` and use the pattern
`<CITY><DATE><ID:03d><SUFFIX>.png`.

Supported fare groups are `B`/`BI` (Bolt), `D`/`DI` (DiDi), and `UX`/`UXI`
(UberX). `UX1` can provide the UberX fare when `UX` is absent. `G` supplies map
distance and duration; `G0` and `G1` are accepted alternatives. When multiple
fare groups are present, the result has one row per route and group. Corrected
screenshots under a `dc/` subfolder take precedence over corresponding
screenshots in the run folder.

Run analysis with the installed command:

```sh
imageparser --phone phone_a --city NYC --date 0906 --analyse
```

Or, from a source checkout without installing the package:

```sh
python src/imageparser/cli.py --phone phone_a --city NYC --date 0906 --analyse
```

`--date 0000` uses today's month/day label. The result is
`ZZ_<CITY>_<DATE>.csv` in the screenshot folder. Legacy app-prefixed city
names such as `BOLT_NYC` are also accepted.

## Reports

Create a self-contained HTML report from one or more result CSVs without an
OCR engine or network access:

```sh
imageparser --report run_a/ZZ_NYC_0906.csv run_b/ZZ_NYC_0906.csv -o compare.html
```

## VS Code

Select the OliverAI interpreter, then use **Run and Debug** and choose
**Analyse SYD_PICKUP 1103 (OliverAI)**. The launch profile runs the CLI in the
integrated terminal and uses `config.example.yaml`.

## Examples

* `examples/01_text_parsing.py` demonstrates OCR text parsing helpers.
* `examples/02_synthetic_analysis.py` demonstrates analysis on a synthetic
  screenshot.
* `examples/04_report.py` generates a report from synthetic results.
