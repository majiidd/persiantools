# Python API Reference

Use this reference for application code or requests that need more than one simple conversion.

## Contents

- [Select the correct type](#select-the-correct-type)
- [Convert dates](#convert-dates)
- [Normalize Persian and Arabic digits](#normalize-persian-and-arabic-digits)
- [Parse named Jalali dates](#parse-named-jalali-dates)
- [Convert datetimes](#convert-datetimes)
- [Format localized output](#format-localized-output)
- [Validate and report errors](#validate-and-report-errors)
- [Verify conversions](#verify-conversions)
- [Convert collections](#convert-collections)
- [Preserve meaning](#preserve-meaning)

## Select the correct type

| Input | PersianTools type | Gregorian type |
| --- | --- | --- |
| Calendar date | `JalaliDate` | `datetime.date` |
| Date and time | `JalaliDateTime` | `datetime.datetime` |

Install the package when needed:

```bash
python -m pip install persiantools
```

## Convert dates

Gregorian to Jalali:

```python
from datetime import date

from persiantools.jdatetime import JalaliDate

source = date.fromisoformat("2024-03-20")
result = JalaliDate.to_jalali(source)
assert result.isoformat() == "1403-01-01"
```

Jalali to Gregorian:

```python
from persiantools.jdatetime import JalaliDate

source = JalaliDate.fromisoformat("1403-01-01")
result = source.to_gregorian()
assert result.isoformat() == "2024-03-20"
```

`JalaliDate.to_jalali(2024, 3, 20)` is also valid when separate numeric fields are already available.

## Normalize Persian and Arabic digits

`JalaliDate.fromisoformat` accepts Persian digits directly. Normalize user input explicitly when it may contain
Arabic-Indic digits or when passing it to a standard-library parser:

```python
from datetime import date

from persiantools import digits
from persiantools.jdatetime import JalaliDate

raw_value = "٢٠٢٤-٠٣-٢٠"
ascii_value = digits.fa_to_en(digits.ar_to_fa(raw_value))
result = JalaliDate.to_jalali(date.fromisoformat(ascii_value))
```

Render any ISO result with Persian digits:

```python
persian_result = digits.en_to_fa(result.isoformat())
```

## Parse named Jalali dates

Use `strptime` instead of maintaining custom parsing logic. PersianTools uses Finglish transliterations for
`locale="en"`.

Months (1–12):

| # | `locale="en"` | `locale="fa"` |
| --- | --- | --- |
| 1 | Farvardin | فروردین |
| 2 | Ordibehesht | اردیبهشت |
| 3 | Khordad | خرداد |
| 4 | Tir | تیر |
| 5 | Mordad | مرداد |
| 6 | Shahrivar | شهریور |
| 7 | Mehr | مهر |
| 8 | Aban | آبان |
| 9 | Azar | آذر |
| 10 | Dey | دی |
| 11 | Bahman | بهمن |
| 12 | Esfand | اسفند |

Weekdays (`isoweekday()`: 1–7; week starts on Shanbeh; `weekday()` is 0–6):

| # | `locale="en"` | `locale="fa"` |
| --- | --- | --- |
| 1 | Shanbeh | شنبه |
| 2 | Yekshanbeh | یکشنبه |
| 3 | Doshanbeh | دوشنبه |
| 4 | Seshanbeh | سه‌شنبه |
| 5 | Chaharshanbeh | چهارشنبه |
| 6 | Panjshanbeh | پنجشنبه |
| 7 | Jomeh | جمعه |

Parse full or abbreviated names with `%B`/`%b` for months and `%A`/`%a` for weekdays:

```python
from persiantools.jdatetime import JalaliDate

english = JalaliDate.strptime("14 Ordibehesht 1367", "%d %B %Y")
persian = JalaliDate.strptime("۱۵ مرداد ۱۴۰۳", "%d %B %Y", locale="fa")
with_weekday = JalaliDate.strptime("Panjshanbeh 15 Mordad 1403", "%A %d %B %Y")
```

Ask for clarification when numeric date order is ambiguous, such as `03/04/1403`.

## Convert datetimes

Preserve time, microseconds, and UTC offsets with `JalaliDateTime`:

```python
from datetime import datetime

from persiantools.jdatetime import JalaliDateTime

gregorian = datetime.fromisoformat("2024-03-20T14:30:15.123456+03:30")
jalali = JalaliDateTime.to_jalali(gregorian)
assert jalali.isoformat() == "1403-01-01T14:30:15.123456+03:30"

restored = JalaliDateTime.fromisoformat(jalali.isoformat()).to_gregorian()
assert restored == gregorian
```

Calendar conversion keeps the local clock fields and `tzinfo`. Convert the timezone separately when requested:

```python
from datetime import timezone

utc_result = jalali.astimezone(timezone.utc)
```

For named zones, use `zoneinfo.ZoneInfo`; do not introduce `pytz`.

## Format localized output

Use `isoformat()` for machine-readable output and `strftime()` for human-readable output:

```python
english_text = jalali.strftime("%A %d %B %Y, %H:%M")
persian_text = jalali.strftime("%A %d %B %Y، %H:%M", locale="fa")
```

Use `locale="fa"` for Persian month and weekday names and Persian digits. Use `locale="en"` for ASCII digits and
transliterated names.

## Validate and report errors

Let constructors and parsers raise `ValueError` for invalid data:

```python
from persiantools.jdatetime import JalaliDate

try:
    result = JalaliDate.fromisoformat(user_value).to_gregorian()
except ValueError as exc:
    # Return a user-facing validation error; do not guess a replacement date.
    raise ValueError(f"Invalid Jalali date: {user_value}") from exc
```

Pay particular attention to Esfand 29/30, Norouz boundaries, Gregorian century leap years, and supported year limits.

## Verify conversions

For application code, round-trip representative values through the opposite conversion:

```python
from datetime import date

from persiantools.jdatetime import JalaliDate

gregorian = date.fromisoformat("2024-03-20")
jalali = JalaliDate.to_jalali(gregorian)

assert jalali.to_gregorian() == gregorian
assert JalaliDate.to_jalali(jalali.to_gregorian()) == jalali
```

Add boundary cases appropriate to the application, especially Norouz, Esfand 29/30, timezone offsets, microseconds,
and Gregorian century leap years. Treat round-trip checks as verification, not as a replacement for input validation.

## Convert collections

Use normal Python iteration so every item still passes through PersianTools:

```python
from datetime import date

from persiantools.jdatetime import JalaliDate

values = ["2024-03-20", "2025-03-21"]
results = [JalaliDate.to_jalali(date.fromisoformat(value)).isoformat() for value in values]
```

For dataframes, databases, web APIs, or large files, keep conversion at the application's boundary and preserve typed
`date` or `datetime` values internally when possible. Do not copy PersianTools calendar algorithms into another layer.

## Preserve meaning

- Treat Jalali, Shamsi, Persian, Iranian, Khorshidi, and Solar Hijri as aliases.
- Treat Gregorian and Miladi as aliases.
- Reject Islamic/lunar Hijri requests as unsupported by this package.
- Preserve date versus datetime precision.
- Distinguish calendar conversion from timezone conversion.
- State assumptions for ambiguous calendar names, numeric date order, locale, or timezone.
