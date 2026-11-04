# Requirements Specification — ImageParser

## 1. Purpose

Parse existing fare screenshots into structured fare, fee, distance, and
duration data using OCR. Device automation and screenshot capture are out of
scope.

## 2. Functional requirements

### FR-1 Image analysis
* FR-1.1 Load route rows from `<work_base>/routes/<CITY>.csv`.
* FR-1.2 Read screenshots from
  `<work_base>/screenshots/<DATE>_<CITY>_<PHONE>/`.
* FR-1.3 Crop screenshots using the selected screen profile and run one OCR
  engine (EasyOCR, PaddleOCR, or Tesseract).
* FR-1.4 Support fare screenshots `B`/`BI`, `D`/`DI`, and `UX`/`UXI`, with
  `UX1` as an alternative UberX fare image. Read map distance and duration from
  `G`, or from `G0`/`G1` when `G` is absent.
* FR-1.5 Prefer matching corrected screenshots in a `dc/` subfolder.
* FR-1.6 Write `ZZ_<CITY>_<DATE>.csv` with the fixed `RESULT_FIELDS` columns
  and cleaned route addresses. Produce one row for every route and each fare
  group present in the run.

### FR-2 Reports
* FR-2.1 Render one or more result CSVs as a self-contained HTML report with
  summary statistics, chart, fee breakdown, data-quality table, and route
  rows.
* FR-2.2 Reports work without an OCR engine or network access.

### FR-3 Configuration
* FR-3.1 Resolve configuration in this order: `--config`,
  `$IMAGEPARSER_CONFIG` (or legacy `$APPAUTOMATION_CONFIG`),
  current-directory `config.yaml`, and bundled `config.example.yaml`.
* FR-3.2 Use the selected phone alias's screen profile and configured OCR
  settings. Retain legacy configuration fields for compatibility.

### FR-4 Command line
* FR-4.1 Analyse with
  `imageparser --phone P --city CITY --date DATE --analyse [--config PATH]`.
  Direct source execution is also supported with
  `python src/imageparser/cli.py`.
* FR-4.2 `--date 0000` means today's month/day label.
* FR-4.3 Create reports with `imageparser --report CSV... [-o PATH]`.

## 3. Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | Runs on Python ≥ 3.9; OCR engines remain optional dependencies |
| NFR-2 | Importing the package does not require an OCR engine |
| NFR-3 | Local configuration and credentials are not committed |
| NFR-4 | Lint and automated tests run with the development dependencies |

## 4. Acceptance criteria

1. `pip install -e ".[dev]" && pytest` passes without a phone or OCR engine.
2. Analysis reads existing route/screenshot files and writes the expected
   result CSV.
3. Reports work offline from result CSVs alone.
4. Explicit, environment, local, and bundled-example configuration sources
   resolve in the documented order.
