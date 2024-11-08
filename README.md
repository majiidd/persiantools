# PersianTools

[![PyPI](https://img.shields.io/pypi/v/persiantools.svg)](https://pypi.org/project/persiantools/)
![test workflow](https://github.com/majiidd/persiantools/actions/workflows/ci.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/majiidd/persiantools/master.svg)](https://results.pre-commit.ci/latest/github/majiidd/persiantools/master)
[![codecov](https://codecov.io/gh/majiidd/persiantools/branch/master/graph/badge.svg?token=Q990VL6FGW)](https://codecov.io/gh/majiidd/persiantools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/persiantools.svg)](https://pypi.org/project/persiantools/)
[![PyPI - License](https://img.shields.io/pypi/l/persiantools.svg)](https://pypi.org/project/persiantools/)

PersianTools provides comprehensive tools for handling Jalali (Shamsi or Persian) dates, date-time functionalities, and more.
- Conversion between Jalali and Gregorian dates/datetimes using Python's native datetime module.
- Full support for operations like `+`, `-`, `==`, and `>=`.
- Timezone-aware date and datetime handling.
- Conversion between Persian and Arabic characters and digits.
- Conversion of numbers to their Persian word representation.

## Install Package
You can install the package using pip with the following command:
```bash
python -m pip install persiantools
```

## Usage Guide

### Date Operations

```python
>>> from persiantools.jdatetime import JalaliDate
>>> import datetime

# Get today's date in Jalali
>>> JalaliDate.today()
JalaliDate(1403, 8, 18, Jomeh)

>>> JalaliDate(1367, 2, 14)
JalaliDate(1367, 2, 14, Chaharshanbeh)

# Convert Gregorian to Jalali
>>> JalaliDate(datetime.date(1988, 5, 4))
JalaliDate(1367, 2, 14, Chaharshanbeh)

# Convert from Gregorian to Jalali using method
>>> JalaliDate.to_jalali(2013, 9, 16)
JalaliDate(1392, 6, 25, Doshanbeh)

# Convert from Jalali to Gregorian
>>> JalaliDate(1392, 6, 25).to_gregorian()
datetime.date(2013, 9, 16)

# Create a Jalali date from a Unix timestamp
>>> JalaliDate.fromtimestamp(578707200)
JalaliDate(1367, 2, 14, Chaharshanbeh)
```

### Datetime Operations

```python
>>> from persiantools.jdatetime import JalaliDateTime
>>> import datetime, pytz

# Get the current Jalali datetime
>>> JalaliDateTime.now()
JalaliDateTime(1403, 8, 18, 12, 48, 54, 569082)

# Convert Jalali datetime to Gregorian
>>> JalaliDateTime.now().to_gregorian()
datetime.datetime(2024, 11, 8, 12, 48, 54, 569082)

# Convert Gregorian datetime to Jalali
>>> JalaliDateTime.to_jalali(datetime.datetime(1988, 5, 4, 14, 0, 0, 0))
JalaliDateTime(1367, 2, 14, 14, 0)

# Create a timezone-aware Jalali datetime from a timestamp
>>> JalaliDateTime.fromtimestamp(578723400, pytz.timezone("Asia/Tehran"))
JalaliDateTime(1367, 2, 14, 8, 0, tzinfo=<DstTzInfo 'Asia/Tehran' +0330+3:30:00 STD>)

>>> JalaliDateTime.now(pytz.utc)
JalaliDateTime(1395, 4, 17, 21, 23, 53, 474618, tzinfo=<UTC>)
```

### Formatting

Based on python `strftime()` behavior

```python
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import pytz

# ISO formatting
>>> JalaliDate(1367, 2, 14).isoformat()
'1367-02-14'

# Custom date formatting
>>> JalaliDate(1395, 3, 1).strftime("%Y/%m/%d")
'1395/03/01'

# Custom datetime formatting
>>> JalaliDateTime(1369, 7, 1, 14, 0, 10, 0, pytz.utc).strftime("%c")
'Yekshanbeh 01 Mehr 1369 14:00:10'
```

### Digits and Character Conversion

```python
>>> from persiantools import characters, digits

# Convert English digits to Persian
>>> digits.en_to_fa("0987654321")
'۰۹۸۷۶۵۴۳۲۱'

# Convert Arabic digits to Persian
>>> digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١")
'۰۹۸۷۶۵۴۳۲۱'

# Convert Persian digits to English
>>> digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱")
'0987654321'

# Convert numbers to Persian words
>>> digits.to_word(9512026)
'نه میلیون و پانصد و دوازده هزار و بیست و شش'

>>> digits.to_word(15.007)
'پانزده و هفت هزارم'

# Convert Arabic to Persian characters
>>> characters.ar_to_fa("كيك")
'کیک'
```

### Operators
The package supports various operators for date and time manipulations. Here are some examples:
```python
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import datetime

>>> JalaliDate(1367, 2, 14) == JalaliDate(datetime.date(1988, 5, 4))
True

>>> JalaliDateTime(1367, 2, 14, 4, 30) >= JalaliDateTime(1368, 2, 14, 1, 0)
False

>>> JalaliDate(1367, 2, 14) == datetime.date(1988, 5, 4)
True

>>> JalaliDate(1395, 2, 14) + datetime.timedelta(days=38)
JalaliDate(1395, 3, 21, Jomeh)

>>> JalaliDateTime(1395, 12, 30) - JalaliDateTime(1395, 1, 1)
datetime.timedelta(365)
```

### Serializing and Deserializing

```python
>>> from persiantools.jdatetime import JalaliDate
>>> import pickle

# Serialize a Jalali date to a file
>>> with open("save.p", "wb") as file:
>>>     pickle.dump(JalaliDate(1367, 2, 14), file)

# Deserialize from a file
>>> with open("save.p", "rb") as file:
>>>     jalali = pickle.load(file)
>>> jalali
JalaliDate(1367, 2, 14, Chaharshanbeh)
```
