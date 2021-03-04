# PersianTools

[![PyPI](https://img.shields.io/pypi/v/persiantools.svg)](https://pypi.org/project/persiantools/)
[![Travis (.com) branch](https://img.shields.io/travis/com/majiidd/persiantools/master)](https://travis-ci.com/github/majiidd/persiantools)
[![AppVeyor](https://ci.appveyor.com/api/projects/status/kau1fi7gp8em94nf/branch/master?svg=true)](https://ci.appveyor.com/project/majiidd/persiantools/branch/master)
[![Coveralls](https://coveralls.io/repos/github/majiidd/persiantools/badge.svg?branch=master)](https://coveralls.io/github/majiidd/persiantools?branch=master)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/persiantools.svg)](https://pypi.org/project/persiantools/)
[![PyPI - License](https://img.shields.io/pypi/l/persiantools.svg)](https://pypi.org/project/persiantools/)

- Jalali (Shamsi) date and datetime (based on python datetime's module)

  - Convert Jalali to Gregorian date/datetime and vice versa
  - Support comparison and arithmetic operators such as `+`, `-`, `==`, `>=`
  - Support timezone

- Convert Arabic and Persian characters/digits to each other
- Convert numbers to words

## Install Package

```{.sourceCode .bash}
python -m pip install persiantools
```
Persiantools supports Python 3.6+. (_for python 2.7 and 3.5 use [1.5.x](https://github.com/majiidd/persiantools/tree/1.5.x) version_)

## How to use

### Date

```{.sourceCode .python}
>>> from persiantools.jdatetime import JalaliDate
>>> import datetime

>>> JalaliDate.today()
JalaliDate(1395, 4, 18, Jomeh)

>>> JalaliDate(1369, 7, 1)
JalaliDate(1369, 7, 1, Yekshanbeh)

>>> JalaliDate(datetime.date(1990, 9, 23))      # Gregorian to Jalali
JalaliDate(1369, 7, 1, Yekshanbeh)

>>> JalaliDate.to_jalali(2013, 9, 16)           # Gregorian to Jalali
JalaliDate(1392, 6, 25, Doshanbeh)

>>> JalaliDate(1392, 6, 25).to_gregorian()      # Jalali to Gregorian
datetime.date(2013, 9, 16)

>>> JalaliDate.fromtimestamp(578707200)         # Timestamp to Jalali
JalaliDate(1367, 2, 14, Chaharshanbeh)
```

### Datetime

```{.sourceCode .python}
>>> from persiantools.jdatetime import JalaliDateTime
>>> import datetime, pytz

>>> JalaliDateTime.now()
JalaliDateTime(1395, 4, 18, 1, 43, 24, 720505)

>>> JalaliDateTime.now().to_gregorian()                                     # Jalali to Gregorian
datetime.datetime(2016, 7, 8, 1, 43, 24, 720505)

>>> JalaliDateTime.to_jalali(datetime.datetime(1988, 5, 4, 14, 0, 0, 0))    # Gregorian to Jalali
JalaliDateTime(1367, 2, 14, 14, 0)

>>> JalaliDateTime.fromtimestamp(578723400, pytz.timezone("Asia/Tehran"))   # Timestamp to Jalali
JalaliDateTime(1367, 2, 14, 8, 0, tzinfo=<DstTzInfo 'Asia/Tehran' +0330+3:30:00 STD>)

>>> JalaliDateTime.now(pytz.utc)
JalaliDateTime(1395, 4, 17, 21, 23, 53, 474618, tzinfo=<UTC>)
```

### Format

Based on python `strftime()` behavior

```{.sourceCode .python}
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import pytz

>>> JalaliDate(1367, 2, 14).isoformat()
'1367-02-14'

>>> JalaliDate(1395, 3, 1).strftime("%Y/%m/%d")
'1395/03/01'

>>> JalaliDateTime(1369, 7, 1, 14, 0, 10, 0, pytz.utc).strftime("%c")
'Yekshanbeh 01 Mehr 1369 14:00:10'

>>> JalaliDateTime.now(pytz.utc).strftime("%I:%M:%S.%f %p %z %Z")
'01:49:22.518523 PM +0000 UTC'
```

### Digits/Characters Tools

```{.sourceCode .python}
>>> from persiantools import characters, digits

>>> digits.en_to_fa("0987654321")
'۰۹۸۷۶۵۴۳۲۱'

>>> digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١")
'۰۹۸۷۶۵۴۳۲۱'

>>> digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱")
'0987654321'

>>> digits.to_word(9512026)
'نه میلیون و پانصد و دوازده هزار و بیست و شش'

>>> characters.ar_to_fa("كيك")
'کیک'
```

### Operators

```{.sourceCode .python}
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import datetime

>>> JalaliDate(1367, 2, 14) == JalaliDate(datetime.date(1988, 5, 4))
True

>>> JalaliDateTime(1367, 2, 14, 4, 30) >= JalaliDateTime(1369, 7, 1, 1, 0)
False

>>> JalaliDate(1367, 2, 14) == datetime.date(1988, 5, 4)
True

>>> JalaliDate(1395, 2, 14) + datetime.timedelta(days=38)
JalaliDate(1395, 3, 21, Jomeh)

>>> JalaliDateTime(1395, 12, 30) - JalaliDateTime(1395, 1, 1)
datetime.timedelta(365)
```

### Serializing and de-serializing

```{.sourceCode .python}
>>> from persiantools.jdatetime import JalaliDate
>>> import pickle

>>> # Serializing
>>> file = open("save.p", "wb")
>>> pickle.dump(JalaliDate(1367, 2, 14), file)
>>> file.close()

>>> # de-serializing
>>> file = open("save.p", "rb")
>>> jalali = pickle.load(file)
>>> file.close()
>>> jalali
JalaliDate(1367, 2, 14, Chaharshanbeh)
```
