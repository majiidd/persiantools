# PersianTools

[![PyPI](https://img.shields.io/pypi/v/persiantools.svg)](https://pypi.org/project/persiantools/)
![test workflow](https://github.com/majiidd/persiantools/actions/workflows/ci.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/majiidd/persiantools/master.svg)](https://results.pre-commit.ci/latest/github/majiidd/persiantools/master)
[![codecov](https://codecov.io/gh/majiidd/persiantools/branch/master/graph/badge.svg?token=Q990VL6FGW)](https://codecov.io/gh/majiidd/persiantools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/persiantools.svg)](https://pypi.org/project/persiantools/)
[![PyPI - License](https://img.shields.io/pypi/l/persiantools.svg)](https://pypi.org/project/persiantools/)

`PersianTools` is a library written in Python for working with Jalali (Persian or Shamsi) dates and times, converting Persian and Arabic characters and digits, and converting numbers to Persian words.

## Key Features

- Conversion between Jalali and Gregorian dates/datetimes using Python's native datetime module.
- Full support for operations such as `+`, `-`, `==`, `>` and `>=`.
- Timezone-aware date and datetime handling.
- Conversion between Persian, Arabic, and English characters and digits.
- Conversion of numbers to their Persian word representation.

## Install Package

You can install the package using `pip` with the following command:

```bash
python -m pip install persiantools
```

## Usage Guide

### Date Operations

The `JalaliDate` object represents a date in the Jalali calendar.

```python
>>> from persiantools.jdatetime import JalaliDate
>>> import datetime

# Today's date
>>> JalaliDate.today()
JalaliDate(1404, 3, 16, Jomeh)

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

# From ISO format
>>> JalaliDate.fromisoformat('1404-01-01')
JalaliDate(1404, 1, 1, Jomeh)

# Create a Jalali date from a Unix timestamp
>>> JalaliDate.fromtimestamp(578707200)
JalaliDate(1367, 2, 14, Chaharshanbeh)

# ISO format output
>>> JalaliDate(1367, 2, 14).isoformat()
'1367-02-14'

# Replace date parts
>>> JalaliDate(1400, 1, 1).replace(month=2, day=10)
JalaliDate(1400, 2, 10, Jomeh)
```
#### Attributes and Methods

```python
>>> date_obj = JalaliDate(1367, 2, 14)

>>> date_obj.year
1367
>>> date_obj.month
2
>>> date_obj.day
14

# Weekday (Saturday is 0 and Friday is 6)
>>> date_obj.weekday() # 1367/2/14 is Chaharshanbeh (Wednesday)
4

# ISO Weekday (Monday is 1 and Sunday is 7)
>>> date_obj.isoweekday()
5

>>> date_obj.week_of_year()
7

# ISO Calendar (ISO year, ISO week number, ISO weekday)
>>> date_obj.isocalendar()
(1367, 7, 5)
```

### Datetime Operations

The `JalaliDateTime` object represents a date and time in the Jalali calendar.

```python
>>> from persiantools.jdatetime import JalaliDateTime
>>> import datetime, pytz

# Current Jalali datetime
>>> JalaliDateTime.now()
JalaliDateTime(1404, 3, 16, 2, 17, 14, 907909)

# Current Jalali datetime (timezone-aware)
>>> JalaliDateTime.now(pytz.timezone("Asia/Tehran"))
JalaliDateTime(1404, 3, 16, 2, 17, 14, 907909, tzinfo=<DstTzInfo 'Asia/Tehran' +0330+3:30:00 STD>)

# Current UTC Jalali datetime
>>> JalaliDateTime.utcnow()
JalaliDateTime(1404, 3, 15, 22, 56, 49, 892339, tzinfo=datetime.timezone.utc)

# Convert Jalali datetime to Gregorian
>>> JalaliDateTime.now().to_gregorian()
datetime.datetime(2025, 6, 6, 2, 17, 14, 907909)

# Convert Gregorian datetime to Jalali (From a datetime.datetime object)
>>> dt_gregorian = datetime.datetime(1988, 5, 4, 14, 30, 15)
>>> JalaliDateTime(dt_gregorian)
JalaliDateTime(1367, 2, 14, 14, 30, 15)

# Replace datetime parts
>>> JalaliDateTime(1400, 1, 1, 12, 0, 0).replace(hour=15, minute=30, microsecond=10)
JalaliDateTime(1400, 1, 1, 15, 30, 0, 10)

# Timezone conversion
>>> tehran_tz = pytz.timezone("Asia/Tehran")
>>> utc_tz = pytz.utc
>>> dt_utc = JalaliDateTime.now(utc_tz)
>>> dt_tehran = dt_utc.astimezone(tehran_tz)
>>> dt_utc
JalaliDateTime(1404, 3, 15, 22, 54, 8, 835877, tzinfo=<UTC>)
>>> dt_tehran
JalaliDateTime(1404, 3, 16, 2, 24, 8, 835877, tzinfo=<DstTzInfo 'Asia/Tehran' +0330+3:30:00 STD>)
```

#### Attributes and Methods

```python
>>> dt_obj = JalaliDateTime(1367, 2, 14, 14, 30, 15, 123, tzinfo=pytz.utc)

>>> dt_obj.year
1367
>>> dt_obj.month
2
>>> dt_obj.day
14
>>> dt_obj.hour
14
>>> dt_obj.minute
30
>>> dt_obj.second
15
>>> dt_obj.microsecond
123
>>> dt_obj.tzinfo
<UTC>

# Date part as datetime.date (Gregorian)
>>> dt_obj.date()
datetime.date(1988, 5, 4)

# JalaliDate object
>>> dt_obj.jdate()
JalaliDate(1367, 2, 14, Chaharshanbeh)

# Time part as datetime.time
>>> dt_obj.time()
datetime.time(14, 30, 15, 123)
```

### Formatting

Based on python `strftime()` behavior

```python
>>> from persiantools.jdatetime import JalaliDateTime
>>> import pytz

>>> dt = JalaliDateTime(1367, 2, 14, 14, 30, 0, tzinfo=pytz.timezone("Asia/Tehran"))

>>> dt.strftime("%Y/%m/%d %H:%M:%S")
'1367/02/14 14:30:00'

>>> dt.strftime("%c", locale='fa')
'چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۱۴:۳۰:۰۰'
```

### Digits and Character Conversion

This section covers converting between different numeral systems (Persian, Arabic, English) and converting numbers to their Persian word representations. It also includes utilities for converting between Persian and Arabic characters.

```python
>>> from persiantools import digits

# Convert English digits to Persian
>>> digits.en_to_fa("0987654321")
'۰۹۸۷۶۵۴۳۲۱'

# Convert Arabic digits to Persian
>>> digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١")
'۰۹۸۷۶۵۴۳۲۱'

# Convert Persian digits to English
>>> digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱")
'0987654321'

# Convert Persian digits to Arabic
>>> digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱")
'٠٩٨٧٦٥٤٣٢١'
```

#### Numbers to Words

Convert numerical values (integers and floats) into Persian words.

```python
>>> from persiantools import digits

>>> digits.to_word(9512026)
'نه میلیون و پانصد و دوازده هزار و بیست و شش'

>>> digits.to_word(15.007)
'پانزده و هفت هزارم'

>>> digits.to_word(-123.45)
'منفی یکصد و بیست و سه و چهل و پنج صدم'

>>> digits.to_word(0)
'صفر'
```

#### Character Conversion

Functions for converting specific Arabic characters to their Persian equivalents and vice-versa. This is often needed due to differences in the Unicode representation of similar-looking characters (e.g., `ک` vs `ك`, `ی` vs `ي`).

```python
>>> from persiantools import characters

>>> characters.ar_to_fa("كيك") # Input uses Arabic Kaf (U+0643) and Yeh (U+064A)
'کیک' # Output uses Persian Keh (U+06A9) and Yeh (U+06CC)

>>> characters.fa_to_ar("کیک")
'كيك'
```

### Operators

Both `JalaliDate` and `JalaliDateTime` objects support standard comparison operators (`<`, `<=`, `==`, `!=`, `>`, `>=`) and arithmetic operations (`+`, `-` with `datetime.timedelta` objects). They can also be compared with their Gregorian counterparts (`datetime.date` and `datetime.datetime`).

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

>>> JalaliDateTime(1395, 2, 14, 12, 0, 0) + datetime.timedelta(hours=5, minutes=30)
JalaliDateTime(1395, 2, 14, 17, 30)
```

### Serializing and Deserializing

`JalaliDate` and `JalaliDateTime` objects can be serialized (pickled) and deserialized (unpickled) using Python's standard `pickle` module. This allows for storing these objects or transmitting them.

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

## Support This Project
If you find this project helpful and would like to support its continued development, please consider donating.

*   **Bitcoin (BTC):** `bc1qg5rp7ymznc98wmhltzvpwl2dvfuvjr33m4hy77`
*   **Tron (TRX):** `TDd63bVWZDBHmwVNFgJ6T2WdWmk9z7PBLg`
*   **Stellar (XLM):** `GDSFPPLY34QSAOTOP4DQDXAI2YDRNRIADZHTN3HCGMQXRLIGPYOEH7L5`
*   **Solana (SOL):** `CXHKgCBqBYy1hbZKGqaSmMzQoTC4Wx2v8QfL9Z7JBo3A`
*   **Dogecoin (DOGE):** `DRZ2QLuXfa5vV1AG83K3XHfYXAHj9b4h4V`
