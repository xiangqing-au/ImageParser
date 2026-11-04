# Test Plan — ImageParser

## Test levels

| Level | Target | Environment |
|-------|--------|-------------|
| Unit | Text parsing, city/path naming, report statistics and HTML output | No device or OCR engine |
| Component | Route/screenshot batch analysis and CLI configuration | Temporary files; OCR engine mocked where needed |
| OCR accuracy | Extraction against a labelled screenshot set | OCR engine installed |

## Automated coverage

Run the suite from the repository root with `pytest`. Tests cover:

* Numeric, fare, and map-summary parsing.
* Legacy city-prefix handling and screenshot path construction.
* CLI analysis using configured work directories and screen profiles.
* Report statistics, CSV loading, HTML escaping, comparisons, and errors.

## OCR accuracy benchmark

Maintain a labelled set of screenshots for each supported fare suffix.
Measure price, distance, duration, and breakdown extraction accuracy, and
compare results with the previous parser/profile before release.
