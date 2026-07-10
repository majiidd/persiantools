# convert-persian-dates

An [Agent Skill](https://agentskills.io) that helps AI agents convert dates and datetimes between the Persian Solar
Hijri calendar (Shamsi, Jalali, Iranian, Persian, or Khorshidi) and Gregorian (Miladi) by calling
[PersianTools](https://github.com/majiidd/persiantools) directly.

The skill contains instructions and an API reference. This keeps PersianTools
as the single source of truth while covering simple questions, Persian and Arabic digits, named months, localization,
validation, timezone-aware datetimes, application integration, and batch conversion.

## Install

Use the cross-agent Skills CLI:

```bash
npx skills add majiidd/persiantools --skill convert-persian-dates
```

Or copy this complete folder into the skills directory supported by your agent. Install the runtime package in the
environment where the agent executes Python:

```bash
python -m pip install persiantools
```

## Ask naturally

```text
امروز چندمه؟
اول امسال به میلادی چه تاریخیه؟
What is today's date in Shamsi?
Convert ۱۴۰۳-۰۱-۰۱ Shamsi to Miladi.
What is 2024-03-20 in the Persian calendar?
Convert ۱۵ مرداد ۱۴۰۳ to Gregorian and explain the result simply.
Show Python code to batch-convert Gregorian dates to Jalali.
Convert this timezone-aware datetime without losing its UTC offset.
```

The agent reads [SKILL.md](SKILL.md) first and loads [references/python-api.md](references/python-api.md) when a request
needs application-level detail.

## License

MIT — see the PersianTools [LICENSE](https://github.com/majiidd/persiantools/blob/master/LICENSE).
