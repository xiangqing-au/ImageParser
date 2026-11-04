# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Direct execution of the CLI source file and a bundled example configuration
  fallback when no local configuration is present.

### Changed
- Renamed the Python package and console command to `imageparser`.
- Documented the current Bolt (`B`/`BI`), DiDi (`D`/`DI`), UberX
  (`UX`/`UXI`/`UX1`), corrected screenshot (`dc/`), and Google Maps
  (`G`/`G0`/`G1`) inputs.
- Updated setup, command-line, configuration, and architecture documentation
  for the screenshot-analysis-only application.

### Removed
- Android device connection, app automation, and screenshot-capture features.
- Capture-only CLI options, capture examples, and device automation dependency.

## [2.1.0] - 2026-10-17

### Added
- **HTML report generator** (`--report`): result CSV(s) → one self-contained
  page with KPI cards, price-per-route bar chart (inline SVG), fee breakdown,
  data-quality table, per-route rows, and a run comparison table when several
  CSVs are passed. No JS, no external assets, works offline.
- `examples/04_report.py`: builds a report from synthetic data, no phone or
  OCR engine required.
- Report tests for statistics, HTML escaping, multi-file comparison, empty
  data, and CLI entry point.
- Process documentation: `docs/REQUIREMENTS.md`, `docs/DESIGN.md`,
  and `docs/TEST_PLAN.md`.
- GitHub Actions CI (ruff + pytest on Python 3.9/3.12), CodeQL workflow,
  Dependabot (pip + actions), coverage summary and artifact per run.
- Issue forms, pull-request template, `CONTRIBUTING.md`, `pre-commit` config.
- `scripts/coverage_summary.py` for CI step summaries.

### Changed
- **Cities are now six US metros** — `NYC`, `LAX`, `CHI`, `SFO`, `HOU`, `MIA`
  with US state abbreviations. Examples, fixtures, route CSVs and docs use
  New York addresses; `CITY_COUNTRIES` stays in place but empty (all bundled
  cities are domestic).
- `--phone/--city/--date/--start/--end` are only required when not running
  `--report`; the error message names the missing flags.
- Packaging metadata: version 2.1.0, classifiers, keywords, project URLs;
  dev extra now includes `pytest-cov` and `ruff`.

### Fixed
- Unused `Dict` import in `runner.py` (found by the new lint gate).

## [2.0.0] - 2026-10-17

### Added
- Package layout under `src/` with `pyproject.toml`
  and optional OCR/development dependency groups.
- CLI entry point for analysis, capture, configuration, and date labels.
- Task naming system (`BOLT_NYC`, `INDRIVE_NYC`, `GOOGLE_LAX`, `TIME_NYC`)
  replacing per-run app lists; `TASK_APPS` / `NO_ANALYSIS_TASKS` tables.
- Google Maps driver: distance and duration, alternative-route capture.
- Scheduled recording mode for `TIME_*` tasks (per-route `hour:minute`).
- `AppNotReadyError` to distinguish "app unusable" from "route failed";
  `RunParams` and dataclass-based configuration.
- Unit tests (12) covering task names, address expansion, price/distance
  parsing and hourly route batching.
- Runnable examples (text parsing, synthetic analysis, and programmatic
  capture) and `docs/GPU_SETUP.md`.

### Changed
- OCR back-ends behind one `OcrEngine` interface with lazy imports; engine
  selected by config (`auto` = first installed).
- Screenshot analysis split into `parser` (per-screen extraction) and
  `analyser` (batch → CSV), with screen profiles per resolution.

## [0.2.0] - 2026-10-17

### Added
- Bolt and inDrive capture modules as real-world examples of multi-page and
  minimal flows.
- Configurable selector prefixes, crop ranges and per-city app sequence.

## [0.1.0] - 2026-10-16

### Added
- Initial public release: capture framework (uiautomator2 over ADB),
  pluggable OCR back-ends, CSV writer, Gmail notifications.

[Unreleased]: https://github.com/OZinOZ/AndroidAppAutomation/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/OZinOZ/AndroidAppAutomation/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/OZinOZ/AndroidAppAutomation/compare/v0.2.0...v2.0.0
[0.2.0]: https://github.com/OZinOZ/AndroidAppAutomation/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/OZinOZ/AndroidAppAutomation/releases/tag/v0.1.0
