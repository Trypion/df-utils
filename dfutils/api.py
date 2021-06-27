import re
from datetime import datetime
from typing import List, Optional, TypeVar

import numpy as np
import pandas as pd
import xlrd
from pandas import DataFrame
from unidecode import unidecode

from dfutils.errors import IrrecognizableValue

T = TypeVar("T")


def _assert_not_none(x: Optional[T]) -> T:
    """Raises AssertionError if input is None, else returns input"""

    if x is not None:
        return x
    raise AssertionError("Expected not None")


def strip_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Removes extra side spaces for entire dataframe"""

    if isinstance(df, DataFrame):
        for col in df.columns:
            df[col] = df[col].str.strip()
        return df

    raise TypeError("DataFrame expected as input")


def clean_dataframe_headers(headers: List[str]) -> List[str]:
    """Removes accents, strips spaces and lowecases list of headers"""

    if isinstance(headers, list) and all(isinstance(el, str) for el in headers):

        return [unidecode(h.strip().lower()) for h in headers]

    raise TypeError("List[str] expected as input")


def extract_date(string: str) -> datetime:
    """Extracts dd.mm.yyyy pattern from string"""

    if not isinstance(string, str):
        raise TypeError("String expected as input")

    return datetime.strptime(
        _assert_not_none(re.search(r"_(\d\d\.\d\d\.\d\d\d\d)\.csv", string)).group(1),
        "%d.%m.%Y",
    )


def standardize_cpf(cpf: str, strict=False) -> str:
    """Removes punctuation from string and prepends zeroes until 11 digits"""

    if not isinstance(cpf, str):
        return str()
    try:
        if not isinstance(cpf, str):
            raise AssertionError(cpf)
        cpf = cpf.replace("'", "")
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")
        return cpf.zfill(11)
    except AssertionError as cpf:
        if strict:
            raise IrrecognizableValue(cpf.__str__())

        return str()


def standardize_date(date: str, strict=False) -> datetime:
    """Standardizes multiple acceptable date formats"""

    if not isinstance(date, str):
        return pd.NaT

    date = date.strip().split(" ")[0]

    try:
        return datetime.strptime(
            _assert_not_none(re.search(r"^(\d{4}-\d{2}-\d{2})$", date)).group(1),
            "%Y-%m-%d",
        )
    except AssertionError:
        pass

    try:
        return datetime.strptime(
            _assert_not_none(re.search(r"^(\d{1,2}/\d{1,2}/\d{4})$", date)).group(1),
            "%d/%m/%Y",
        )
    except AssertionError:
        pass

    try:
        return datetime.strptime(
            _assert_not_none(re.search(r"^(\d{1,2}/\d{1,2}/\d{2})$", date)).group(1),
            "%d/%m/%y",
        )
    except AssertionError:
        pass

    try:
        return xlrd.xldate_as_datetime(int(date), 0)
    except ValueError:
        pass

    if strict:
        raise IrrecognizableValue(date)

    return pd.NaT


def standardize_values(val: str, strict=False) -> float:
    """Standardizes multiple acceptable money formats"""

    if not isinstance(val, str):
        return np.NaN
    val = val.upper().replace("R$", "").strip()

    try:
        return float(int(val))
    except ValueError:
        pass

    if (
        match := re.search(
            r"^(\d{1,})(?:,|\.)(\d{1,2})$",
            val,
        )
    ) and len(groups := match.groups()) == 2:
        integer = groups[0]
        decimal = groups[1]
        return float(f"{integer}.{decimal}")

    if (
        match := re.search(
            r"^(\d{1,3}(?:(?:\.(?:\d{3}))+|(?:,(?:\d{3}))+))$",
            val,
        )
    ) and len(groups := match.groups()) == 1:
        integer = groups[0].replace(".", "").replace(",", "")
        decimal = "00"
        return float(f"{integer}.{decimal}")

    if (
        match := re.search(
            r"^(\d{1,3}(?:\.\d{3}){0,}),(\d{1,2})$",
            val,
        )
    ) and len(groups := match.groups()) == 2:
        integer = groups[0].replace(".", "")
        decimal = groups[1]
        return float(f"{integer}.{decimal}")

    if (
        match := re.search(
            r"^(\d{1,3}(?:,\d{3}){0,})\.(\d{1,2})$",
            val,
        )
    ) and len(groups := match.groups()) == 2:
        integer = groups[0].replace(",", "")
        decimal = groups[1]
        return float(f"{integer}.{decimal}")

    if (
        match := re.search(
            r"^(\d{1,})(?:,|\.)(\d{4,})$",
            val,
        )
    ) and len(groups := match.groups()) == 2:
        integer = groups[0]
        decimal = groups[1]
        return round(float(f"{integer}.{decimal}"), 2)

    if strict:
        raise IrrecognizableValue(val)

    return np.NaN
