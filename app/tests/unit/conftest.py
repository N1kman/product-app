import json
from pathlib import Path

import pytest


def get_test_data(filename):
    path = Path(__file__).parent / 'test_data' / filename
    with open(path) as file:
        return json.load(file)


@pytest.fixture
def get_product_data():
    return get_test_data("product.json")
