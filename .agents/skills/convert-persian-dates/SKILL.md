---
name: convert-persian-dates
description: Convert dates and datetimes between the Persian Solar Hijri calendar (Shamsi, Jalali, Iranian, Khorshidi) and the Gregorian (Miladi) calendar — including current and relative dates, Persian or Arabic-Indic digits, named Persian months and weekdays, ISO strings, timezone-aware values, formatting, and batch or in-code conversion. Use this skill whenever the user supplies or asks for a Persian/Shamsi/Jalali date, or wants a Gregorian date expressed in the Persian calendar, even if they do not say "convert" or name the calendar (for example "1403/01/01", "today in Shamsi", or "when is Nowruz 1404"). Do not use for Islamic or lunar (Qamari) Hijri dates, a different calendar this skill cannot convert.
---

# Convert Persian Dates

Call the installed `persiantools` package directly. Never implement calendar arithmetic.

## Follow the default procedure

1. Establish the source calendar, target calendar, and whether the value is a date or datetime.
2. Use `JalaliDate` for dates and `JalaliDateTime` for values containing a time.
3. For a simple ISO value, run the matching direct command below after substituting the user's value.
4. Load only the relevant section of [references/python-api.md](references/python-api.md) when the request needs named
   dates, digit normalization, localization, application code, batch conversion, validation, or timezone handling.
5. Verify the result with the checklist below.
6. Return a concise answer adapted to the user's technical level.

## Prepare the environment

Use the active Python environment and check whether `persiantools` imports. Do not change a project merely to answer a
one-off question. If the package is missing, ask before installing it. For application integration, use the project's
existing package manager; otherwise the default is:

```bash
python -m pip install persiantools
```

For a nontechnical user, perform the conversion and omit setup details unless setup blocks the result.

## Convert simple ISO values

Gregorian to Jalali:

```bash
python -c "from datetime import date; from persiantools.jdatetime import JalaliDate; print(JalaliDate.to_jalali(date.fromisoformat('2024-03-20')).isoformat())"
```

Jalali to Gregorian, including Persian digits:

```bash
python -c "from persiantools.jdatetime import JalaliDate; print(JalaliDate.fromisoformat('۱۴۰۳-۰۱-۰۱').to_gregorian().isoformat())"
```

Current Jalali date:

```bash
python -c "from persiantools.jdatetime import JalaliDate; print(JalaliDate.today().isoformat())"
```

Keep one-off commands small enough to inspect. For multi-step or application code, use the API reference instead of an
oversized shell command.

## Gotchas

- Treat Shamsi, Jalali, Iranian, Persian, Khorshidi, and Solar Hijri as the same calendar; treat Gregorian and Miladi as
  the same calendar.
- Do not treat Islamic or lunar Hijri as Persian Solar Hijri; PersianTools does not convert lunar Hijri dates.
- Treat a year such as 1403 or 2024 as a clue, not proof of the calendar. Ask when ambiguity could change the answer.
- Let PersianTools reject invalid dates. Never repair a date silently or assume Esfand always has 30 days.
- Preserve seconds, microseconds, and `tzinfo`. Calendar conversion does not change timezones; use `astimezone()` only
  when the user requests a timezone conversion.
- `locale="en"` uses Finglish Jalali names such as `Farvardin` and `Shanbeh`, not Gregorian names.
- Resolve “today” and “now” from the real system clock, never model memory.

## Verify before answering

1. Confirm the package call completed without a parsing or range error.
2. Confirm the output calendar and returned type match the request.
3. For datetimes, confirm time precision and the UTC offset or `tzinfo` were retained.
4. For batch or application code, test a representative round trip and relevant boundaries such as Norouz and Esfand
   29/30 before recommending the implementation.
5. If validation fails, report the input problem and request a correction; do not guess.

## Return the answer

For a plain-language request, adapt this template to the user's language:

```text
[input] [source calendar] equals [result] [target calendar].
```

For a developer request, lead with the result or API choice, then include only the smallest useful code sample. Prefer
ISO `YYYY-MM-DD` or ISO datetime output unless another format is requested. State any assumption about an ambiguous
calendar, date order, locale, or timezone.
