# Contributing

Thanks for contributing to the screenshot image parser.

## Setup

```bash
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"                           # package + pytest + ruff
pip install -e ".[tesseract]"                     # or install the easyocr/paddle extra
pytest                                            # no device or OCR engine needed for tests
```

Install the Tesseract executable separately and make it available on `PATH`.
The CLI uses `config.yaml` if present, otherwise `config.example.yaml`.
`config.yaml`, `credentials.json`, and `token.json` should not be committed.

## Definition of done

A change is ready when **all** of these hold:

1. `pytest` passes and new logic comes with a test (see `tests/` for the style).
2. `ruff check --select E9,F src tests examples` is clean.
3. User-visible behaviour is documented: `README.md` for usage, `docs/` for
   design or process, `CHANGELOG.md` under `[Unreleased]`.
4. No secrets, serials or personal paths in the diff.

## Reporting problems

For parser bugs, include the input suffix and attach
a cropped screenshot if you can — it is usually the fastest way to see
whether the profile or parser is wrong.

## Commit style

Short imperative subject (`Improve fare extraction`, `Fix route parsing`),
body explaining *why* when the change is not obvious. Keep unrelated
refactors out of functional commits.
