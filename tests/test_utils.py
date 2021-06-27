from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
import dfutils as utils


def test_standardize_values() -> None:
    cases = {
        "1": 1.0,
        "1234567890": 1234567890,
        "12,34": 12.34,
        "12.34": 12.34,
        "1.234": 1234,
        "12.345": 12345,
        "1234.456": np.NaN,
        "1,234": 1234,
        "12,345": 12345,
        "1234,456": np.NaN,
        "1.234,456": np.NaN,
        "1,234.567": np.NAN,
        "1.234,56": 1234.56,
        "1.234.567,89": 1234567.89,
        "1.234.567.890,12": 1234567890.12,
        "1234.5699999": 1234.57,
        "123,5600000": 123.56,
        "1.23,45": np.NaN,
        "1.2345,67": np.NaN,
        "1.234,5": 1234.5,
        "1.234,567": np.NaN,
        "1,234.56": 1234.56,
        "1,234,567.89": 1234567.89,
        "1,234,567,890.12": 1234567890.12,
        "1,23.45": np.NaN,
        "1,2345.67": np.NAN,
        "1,234.5": 1234.5,
        "1.234.56": np.NaN,
        "1,234,56": np.NaN,
        "1.234.": np.NaN,
        "1,234,": np.NaN,
        "R$1": 1.0,
        "R$ 1,23": 1.23,
        "NotNumber": np.NaN,
        pd.NA: np.NaN,
    }

    for key, value in cases.items():
        if np.isnan(value):
            assert np.isnan(utils.standardize_values(key))
        else:
            assert utils.standardize_values(key) == value


def test_standardize_date() -> None:
    cases = {
        "01/02/2000": datetime(2000, 2, 1),
        "01/2/2000": datetime(2000, 2, 1),
        "1/02/2000": datetime(2000, 2, 1),
        "1/2/2000": datetime(2000, 2, 1),
        "01/02/00": datetime(2000, 2, 1),
        "2000-02-01": datetime(2000, 2, 1),
        "2000-1-1": pd.NaT,
        "01/02/20000": pd.NaT,
        "01//20": pd.NaT,
        pd.NA: pd.NaT,
    }

    for key, value in cases.items():
        if pd.isnull(value):
            assert pd.isnull(utils.standardize_date(key))
        else:
            assert utils.standardize_date(key) == value


def test_standardize_cpf() -> None:
    cases = {
        "'123.456.789-10": "12345678910",
        "123.456.789-01": "12345678901",
        "12345678901": "12345678901",
        "000000123-45": "00000012345",
        pd.NA: "",
    }

    for key, value in cases.items():
        assert utils.standardize_cpf(key) == value


def test_extract_dates_success() -> None:
    cases = {
        "Bradesco_01.02.2000.csv": datetime(2000, 2, 1),
        "c6_01.02.2000.csv": datetime(2000, 2, 1),
    }

    for key, value in cases.items():
        assert utils.extract_date(key) == value


def test_extract_dates_error() -> None:
    cases = [
        "Bradesco01.02.2000.csv",
        "Bradesco_01.2.2000.csv",
        "c6_01.02.20000.csv",
        "c6_01_02_2000.csv",
    ]

    for value in cases:
        with pytest.raises(AssertionError) as e:
            utils.extract_date(value)
        assert str(e.value) == "Expected not None"


def test_clean_dataframe_headers() -> None:
    headers = ["Aa", "Èé", "Àà", "Ôô", "Ãã", "Çç", "  Aa  "]
    expected = ["aa", "ee", "aa", "oo", "aa", "cc", "aa"]
    assert utils.clean_dataframe_headers(headers) == expected


def test_strip_dataframe(df: pd.DataFrame) -> None:
    df_with_stripped_columns = pd.DataFrame(
        {
            "Col_A": [123, 456, None],
            "Col_B": ["sample", "", "dataframe"],
            "Col_C": [None, "hello", "world"],
        },
        dtype="string",
    )
    assert_frame_equal(utils.strip_dataframe(df), df_with_stripped_columns)
