import pytest
from pandas import DataFrame


@pytest.fixture(scope="session")
def df() -> DataFrame:
    return DataFrame(
        {
            "Col_A": [123, 456, None],
            "Col_B": ["  sample", "", "dataframe   "],
            "Col_C": [None, "hello", "  world  "],
        },
        dtype="string",
    )
