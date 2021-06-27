# dfutils
Helper functions for transforming data in pandas Dataframes.

## Features
- stripping spaces

Removes extra side spaces for entire Dataframe.
```
>>> df = pd.DataFrame()
>>> df["hello"] = pd.Series(["   strings  ", "with  ", "   spaces"])
>>> df = dfutils.strip_dataframe(df)
>>> df["hello"].tolist()
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
>>> df["hello"] = pd.Series(["2021-01-01", "01/01/2021", "01/01/21"])
>>> df["hello"] = pd.Series(["2021-02-01", "01/02/2021", "01/02/21"])
>>> df["hello"] = df["hello"].apply(dfutils.standardize_date)
>>> df["hello"].tolist()
[Timestamp('2021-02-01 00:00:00'), Timestamp('2021-02-01 00:00:00'), Timestamp('2021-02-01 00:00:00')]
```

- standardize values

Standardizes multiple acceptable monetary values.
```
>>> df = pd.DataFrame()
>>> df["hello"] = pd.Series(["1000", "1,000.00", "1.000,00", "1000.00", "1000,00"])
>>> df["hello"] = df["hello"].apply(dfutils.standardize_values)
>>> df["hello"].tolist()
[1000.0, 1000.0, 1000.0, 1000.0, 1000.0]
```
- standardize cpf

Removes punctuation from string and prepends zeroes until 11 digits.
```
>>> df = pd.DataFrame()
>>> df["hello"] = pd.Series(["123.345.789-10", "1234567"])
>>> df["hello"] = df["hello"].apply(dfutils.standardize_cpf)
>>> df["hello"].tolist()
['12334578910', '00001234567']
```