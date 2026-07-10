# PersianTools

[![PyPI](https://img.shields.io/pypi/v/persiantools.svg)](https://pypi.org/project/persiantools/)
![test workflow](https://github.com/majiidd/persiantools/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/majiidd/persiantools/branch/master/graph/badge.svg?token=Q990VL6FGW)](https://codecov.io/gh/majiidd/persiantools)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/persiantools.svg)](https://pypi.org/project/persiantools/)
[![PyPI - License](https://img.shields.io/pypi/l/persiantools.svg)](https://pypi.org/project/persiantools/)

`PersianTools` provides Jalali (Shamsi) dates and datetimes that work just like Python's `datetime` — plus handy tools for Persian text: digit conversion between Persian, Arabic, and English, character normalization, and numbers to Persian words.

If you know `datetime.date` and `datetime.datetime`, you already know `JalaliDate` and `JalaliDateTime`. They support the same operations: comparison, arithmetic with `timedelta`, timezones, `strftime`/`strptime` and formatting, hashing, and pickling.

## Installation

```bash
pip install persiantools
```

Requires Python 3.9 or newer. No dependencies, except `tzdata` on Windows for timezone data.

## Quick start

```python
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import datetime

>>> JalaliDate.today()
JalaliDate(1405, 4, 12, Jomeh)

>>> JalaliDate(datetime.date(1988, 5, 4))       # Gregorian → Jalali
JalaliDate(1367, 2, 14, Chaharshanbeh)

>>> JalaliDate(1367, 2, 14).to_gregorian()      # Jalali → Gregorian
datetime.date(1988, 5, 4)

>>> JalaliDateTime.now().strftime("%A %d %B %Y, %H:%M")
'Jomeh 12 Tir 1405, 14:30'
```

## Dates

Create a `JalaliDate` from Jalali values, a Gregorian date, an ISO string, or a timestamp:

```python
>>> from persiantools.jdatetime import JalaliDate
>>> import datetime

>>> JalaliDate(1367, 2, 14)
JalaliDate(1367, 2, 14, Chaharshanbeh)

>>> JalaliDate.to_jalali(2013, 9, 16)
JalaliDate(1392, 6, 25, Doshanbeh)

>>> JalaliDate.fromisoformat("1404-01-01")
JalaliDate(1404, 1, 1, Jomeh)

>>> JalaliDate.fromtimestamp(578707200)
JalaliDate(1367, 2, 14, Chaharshanbeh)

>>> JalaliDate(1400, 1, 1).replace(month=2, day=10)
JalaliDate(1400, 2, 10, Jomeh)
```

The week starts on Shanbeh (Saturday). `weekday()` counts from 0 (Shanbeh) to 6 (Jomeh), and `isoweekday()` from 1 to 7:

```python
>>> d = JalaliDate(1367, 2, 14)  # a Chaharshanbeh (Wednesday)
>>> d.weekday()
4
>>> d.isoweekday()
5
>>> d.isocalendar()
IsoCalendarDate(year=1367, week=7, weekday=5)
>>> d.isoformat()
'1367-02-14'
```

## Datetimes

`JalaliDateTime` adds time and timezone support on top of `JalaliDate`:

```python
>>> from persiantools.jdatetime import JalaliDateTime
>>> from zoneinfo import ZoneInfo
>>> import datetime

>>> JalaliDateTime.now(ZoneInfo("Asia/Tehran"))
JalaliDateTime(1405, 4, 12, 14, 30, 7, 907909, tzinfo=zoneinfo.ZoneInfo(key='Asia/Tehran'))

>>> JalaliDateTime(datetime.datetime(1988, 5, 4, 14, 30, 15))
JalaliDateTime(1367, 2, 14, 14, 30, 15)

>>> JalaliDateTime(1367, 2, 14, 14, 30, 15).to_gregorian()
datetime.datetime(1988, 5, 4, 14, 30, 15)

>>> JalaliDateTime(1367, 2, 14, 14, 30, tzinfo=datetime.timezone.utc).isoformat(timespec="minutes")
'1367-02-14T14:30+00:00'
```

## Formatting and parsing

Both classes support `strftime` and `strptime` with the familiar directives, in English or Persian:

```python
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime

>>> JalaliDate(1367, 2, 14).strftime("%A %d %B %Y")
'Chaharshanbeh 14 Ordibehesht 1367'

>>> JalaliDateTime(1367, 2, 14, 14, 30).strftime("%c", locale="fa")
'چهارشنبه ۱۴ اردیبهشت ۱۳۶۷ ۱۴:۳۰:۰۰'

>>> JalaliDate.strptime("1367-02-14", "%Y-%m-%d")
JalaliDate(1367, 2, 14, Chaharshanbeh)

>>> JalaliDateTime.strptime("1367/02/14 14:30", "%Y/%m/%d %H:%M")
JalaliDateTime(1367, 2, 14, 14, 30)
```

A date created with `locale="fa"` renders itself with Persian digits and names everywhere:

```python
>>> JalaliDate(1367, 2, 14, locale="fa").isoformat()
'۱۳۶۷-۰۲-۱۴'
```

## Comparison and arithmetic

Jalali objects compare and do arithmetic with each other, with `timedelta`, and directly with their Gregorian counterparts:

```python
>>> from persiantools.jdatetime import JalaliDate, JalaliDateTime
>>> import datetime

>>> JalaliDate(1367, 2, 14) == datetime.date(1988, 5, 4)
True

>>> JalaliDate(1395, 2, 14) + datetime.timedelta(days=38)
JalaliDate(1395, 3, 21, Jomeh)

>>> JalaliDateTime(1395, 12, 30) - JalaliDateTime(1395, 1, 1)
datetime.timedelta(days=365)

>>> JalaliDate(1399, 12, 30) > JalaliDate(1399, 12, 29)   # leap-year Esfand 30
True
```

They are also hashable (usable as dict keys) and picklable, like the standard library types.

## Digits

Convert digits between English, Persian, and Arabic:

```python
>>> from persiantools import digits

>>> digits.en_to_fa("0987654321")
'۰۹۸۷۶۵۴۳۲۱'

>>> digits.ar_to_fa("٠٩٨٧٦٥٤٣٢١")
'۰۹۸۷۶۵۴۳۲۱'

>>> digits.fa_to_en("۰۹۸۷۶۵۴۳۲۱")
'0987654321'

>>> digits.fa_to_ar("۰۹۸۷۶۵۴۳۲۱")
'٠٩٨٧٦٥٤٣٢١'
```

And spell numbers out in Persian — integers, floats, and negatives:

```python
>>> digits.to_word(9512026)
'نه میلیون و پانصد و دوازده هزار و بیست و شش'

>>> digits.to_word(15.007)
'پانزده و هفت هزارم'

>>> digits.to_word(-123.45)
'منفی یکصد و بیست و سه و چهل و پنج صدم'
```

## Characters

Arabic and Persian share letters that look alike but have different Unicode code points (`ك` vs `ک`, `ي` vs `ی`) — a common source of failed string matching and broken search. Normalize them in either direction:

```python
>>> from persiantools import characters

>>> characters.ar_to_fa("كيك")
'کیک'

>>> characters.fa_to_ar("کیک")
'كيك'
```

## Support this project

If persiantools saves you time, you can support its development with a donation:

| Coin | Address |
| --- | --- |
| Bitcoin (BTC) | `bc1qg5rp7ymznc98wmhltzvpwl2dvfuvjr33m4hy77` |
| Ethereum (ETH) | `0xC7D6bf306E456632764D0aD111C8dBBb43a3B9ad` |
| Tron (TRX) | `TDd63bVWZDBHmwVNFgJ6T2WdWmk9z7PBLg` |
| Stellar (XLM) | `GDSFPPLY34QSAOTOP4DQDXAI2YDRNRIADZHTN3HCGMQXRLIGPYOEH7L5` |
| USDT (BSC) | `0xC7D6bf306E456632764D0aD111C8dBBb43a3B9ad` |

## AI Agent Skill

Need your AI assistant to convert Persian (Shamsi/Jalali) dates accurately? Install the
[`convert-persian-dates`](.agents/skills/convert-persian-dates/SKILL.md) — it teaches the agent to convert between
Shamsi and Gregorian (Miladi) without guessing calendar math.

```bash
npx skills add majiidd/persiantools --skill convert-persian-dates
```

Add `--global` to enable it across all projects. OpenAI Codex and Cursor also pick it up automatically when this
repo is open. After install, ask naturally:

```text
امروز چندمه؟
What is today's date in Shamsi?
Convert 1405-01-01 Shamsi to Gregorian.
```

The skill needs `pip install persiantools` in the environment where the agent runs Python.
