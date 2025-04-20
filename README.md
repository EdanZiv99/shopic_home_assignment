# Shopic Home Assignment – Test Automation Framework

This project implements an automated testing system for validating CSV uploads to a FastAPI-based product ingestion server.  
The tests cover valid uploads, invalid data handling, and edge cases using Playwright, pytest, and the Page Object Model (POM) pattern.

## Setup Instructions

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies (customized requirements.txt):

```bash
pip install -r requirements.txt
```

Note: `pytest==7.4.3` was used instead of the originally provided `pytest==8.3.4` due to a version conflict with `pytest-playwright`.  
To preserve compatibility, pytest was downgraded and `pytest-asyncio` was added manually.

3. Install Playwright browsers:

```bash
python -m playwright install
```

## Test Execution Instructions

Run all tests with:

```bash
pytest tests/ -v -o log_cli=true --log-cli-level=INFO
```

To generate an HTML report (as required):

```bash
pytest tests/ --html=report.html --self-contained-html
```

This report summarizes test results across valid and invalid.

## Project Structure

```
home_assignment/
├── pages/                    ← Page Object Model abstraction
│   └── upload_page.py
├── tests/
│   ├── test_valid_uploads.py        ← Valid file tests
│   ├── test_invalid_uploads.py      ← Invalid + edge case tests
│   ├── test_helpers.py              ← Shared logic (browser handling)
│   └── conftest.py                  ← Path config for imports
├── data/                     ← Input test CSV files + expected output
│   ├── valid_*.csv
│   ├── invalid_*.csv
│   └── expected_results.json
├── app.py                    ← Provided server (not modified)
├── requirements.txt
└── report.html               ← Generated test report
```

## Test Coverage

The tests cover:
- Valid uploads: ensuring that all rows are accepted and returned correctly
- Invalid uploads: verifying validation logic (e.g., missing name, invalid price)
- Edge cases: e.g., empty file, only headers, single column

Each file is matched to expected output using a shared `expected_results.json` file.

## Assumptions and Limitations

- CSV Classification is done dynamically based on `error_count` in `expected_results.json`, not by filename convention.
- Edge cases are treated as valid or invalid based on expected behavior, not hard-coded assumptions.
- The test logic supports both formats of error responses from the server:
  - "errors": [ ... ] for row-level errors
  - "message": "..." for general parsing issues

## Notable Adjustments and Findings

### requirements.txt Change
A version conflict existed between:
- pytest==8.3.4 (initially required)
- pytest-playwright==0.4.3 (which supports only pytest<8.0.0)

To resolve this, I used:
```
pytest==7.4.3
pytest-playwright==0.4.3
pytest-asyncio==0.23.5
```

### Server Logic Inconsistency
One of the tests (`invalid_products.csv`) revealed an inconsistency in the server’s validation logic:

The server flagged "price": 89.99 as invalid even though it’s a valid number, because it was typed as a string.

Root cause:
```python
if not isinstance(row["price"], (int, float)) or row["price"] < 0:
```

Suggested fix:
```python
try:
    price = float(row["price"])
    if price < 0:
        ...
except ValueError:
    ...
```

I kept the test unchanged to surface this logical flaw as part of the validation coverage.

## Final Notes

- The framework was designed to be robust, modular, and extensible.
- The test cases are declarative via `expected_results.json`, making it easy to add/remove files.
- Logging, error handling, and HTML reports are all integrated and production-grade.
