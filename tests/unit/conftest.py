import os
import sys

import pytest

# Add Lambda directory to Python path so tests can import stonksfeed
LAMBDA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "infrastructure", "lambdas", "fetch_rss"
)
sys.path.insert(0, LAMBDA_DIR)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def content_data(request):
    file_name = request.param
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "r") as infile:
        data = infile.read()
    return data
