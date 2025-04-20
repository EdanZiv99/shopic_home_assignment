import pytest
import json
import logging
from pathlib import Path
from tests.test_helpers import run_upload_test

# Enable log output to terminal
logging.basicConfig(level=logging.INFO)

# Set paths
data_dir = Path(__file__).parent.parent / "data"
expected_path = data_dir / "expected_results.json"

# Load expected results from shared file
with expected_path.open() as f:
    expected_all = json.load(f)

# Select only CSV files expected to succeed (no errors)
csv_files = [
    data_dir / (key + ".csv")
    for key, val in expected_all.items()
    if val.get("error_count", 0) == 0
]

@pytest.mark.asyncio
@pytest.mark.parametrize("csv_path", csv_files)
async def test_valid_file(csv_path: Path):
    """
    Validates that the given CSV file uploads successfully and returns the expected number of valid rows.
    """
    key = csv_path.stem
    expected = expected_all[key]

    logging.info(f"Testing VALID file: {csv_path.name}")

    try:
        # Run upload and get parsed server response
        actual = await run_upload_test(csv_path)

        # Validate the status and the number of returned rows
        assert actual["status"] == "success"
        assert len(actual["data"]) == expected["success_count"]
        assert len(actual["data"]) == expected["total"], (
            f"Expected total {expected['total']} but got {len(actual['data'])} rows"
        )

        logging.info(f"{csv_path.name} passed with {len(actual['data'])} records.")

    except Exception as e:
        logging.error(f"Unexpected error for {csv_path.name}: {e}")
        assert False, f"Unexpected error: {e}"
