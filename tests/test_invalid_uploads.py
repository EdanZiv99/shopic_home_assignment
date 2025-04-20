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

# Select only CSV files expected to fail validation (error_count > 0)
csv_files = [
    data_dir / (key + ".csv")
    for key, val in expected_all.items()
    if val.get("error_count", 0) > 0
]

@pytest.mark.asyncio
@pytest.mark.parametrize("csv_path", csv_files)
async def test_invalid_file(csv_path: Path):
    """
    Tests that an invalid CSV file fails validation as expected.
    The server is expected to return a response with "status": "error".
    This test handles two types of error responses:
    - A list of row-level validation errors (under "errors")
    - A general file-level error message (under "message")
    """
    key = csv_path.stem
    expected = expected_all[key]

    logging.info(f"Testing INVALID file: {csv_path.name}")

    try:
        # Run upload and get parsed server response
        actual = await run_upload_test(csv_path)

        # Ensure the status is "error"
        assert actual["status"] == "error"

        # Handle validation-type errors (per row)
        if "errors" in actual:
            assert actual["errors"] == expected["expected_errors"]

        # Handle general parsing/file errors
        elif "message" in actual:
            if "expected_message" in expected:
                assert actual["message"] == expected["expected_message"]

        # Fail if neither errors nor message exist
        else:
            assert False, "No 'errors' or 'message' field returned by server"

        logging.info(f"{csv_path.name} correctly failed.")

    except Exception as e:
        logging.error(f"Unexpected error for {csv_path.name}: {e}")
        assert False, f"Unexpected error: {e}"
