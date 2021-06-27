# dfutils
Helper functions for transforming data in pandas Dataframes.

## How to use
Install from this repository.
```
pip install git+https://github.com/alancampag/df-utils
```
Import the module.
```
import dfutils
``` 

## Features
- stripping spaces

Removes extra side spaces for entire Dataframe.
```
>>> df = pd.DataFrame()
>>> df["dates"] = pd.Series(["   strings  ", "with  ", "   spaces"])
>>> df = dfutils.strip_dataframe(df)
>>> df["dates"].tolist()
['strings', 'with', 'spaces']
```
- cleaning headers

Removes accents, strips spaces and lowecases each element in list of headers (or any other Python list).
```
>>> df = pd.DataFrame(columns=["heLLo  ", "  wórLD"])
>>> df.columns
Index(['heLLo  ', '  wórLD'], dtype='object')

>>> df.columns = dfutils.clean_dataframe_headers(list(df.columns))
>>> df.columns
Index(['hello', 'world'], dtype='object')
```
- standardize dates

Standardizes multiple acceptable brazilian date formats.
```
>>> df = pd.DataFrame()
>>> df["dates"] = pd.Series(["2021-01-01", "01/01/2021", "01/01/21"])
>>> df["dates"] = df["dates"].apply(dfutils.standardize_date)
>>> df["dates"].tolist()
[Timestamp('2021-02-01 00:00:00'), Timestamp('2021-02-01 00:00:00'), Timestamp('2021-02-01 00:00:00')]
```

- standardize values

Standardizes multiple acceptable monetary values.
```
>>> df = pd.DataFrame()
>>> df["value"] = pd.Series(["1000", "1,000.00", "1.000,00", "1000.00", "1000,00"])
>>> df["value"] = df["value"].apply(dfutils.standardize_values)
>>> df["value"].tolist()
[1000.0, 1000.0, 1000.0, 1000.0, 1000.0]
```
- standardize cpf

Removes punctuation from string and prepends zeroes until 11 digits.
```
>>> df = pd.DataFrame()
>>> df["cpfs"] = pd.Series(["123.345.789-10", "1234567"])
>>> df["cpfs"] = df["cpfs"].apply(dfutils.standardize_cpf)
>>> df["cpfs"].tolist()
['12334578910', '00001234567']
```