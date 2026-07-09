import gc
import os
import statistics
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from time import perf_counter_ns
from typing import Callable

import pytest

from persiantools import characters, digits
from persiantools.jdatetime import JalaliDate, JalaliDateTime

pytestmark = pytest.mark.skipif(
    not os.environ.get("PERSIANTOOLS_PERF_TESTS"),
    reason="set PERSIANTOOLS_PERF_TESTS=1 to run opt-in performance tests",
)


@dataclass(frozen=True)
class PerfCase:
    name: str
    operation: Callable[[], int]
    iterations: int
    max_us_per_op: float


def _measure(case: PerfCase, rounds: int = 7) -> tuple[float, float]:
    expected = case.operation()
    samples = []
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(rounds):
            start = perf_counter_ns()
            result = case.operation()
            elapsed_ns = perf_counter_ns() - start
            assert result == expected
            samples.append(elapsed_ns / case.iterations / 1_000)
    finally:
        if gc_was_enabled:
            gc.enable()

    best = min(samples)
    median = statistics.median(samples)
    print(f"{case.name}: best={best:.3f} us/op, median={median:.3f} us/op, " f"budget={case.max_us_per_op:.3f} us/op")
    return best, median


def _make_perf_cases() -> tuple[PerfCase, ...]:
    gregorian_dates = tuple(date(1970, 1, 1) + timedelta(days=step * 17) for step in range(4096))
    jalali_dates = tuple(JalaliDate.to_jalali(item) for item in gregorian_dates)
    gregorian_datetimes = tuple(
        datetime(
            item.year,
            item.month,
            item.day,
            hour=index % 24,
            minute=index % 60,
            second=(index * 7) % 60,
            microsecond=(index * 37) % 1_000_000,
            tzinfo=timezone.utc,
        )
        for index, item in enumerate(gregorian_dates)
    )
    jalali_datetimes = tuple(JalaliDateTime.to_jalali(item) for item in gregorian_datetimes)
    formatted_datetimes = tuple(item.strftime("%Y-%m-%d %H:%M:%S.%f %z") for item in jalali_datetimes[:1024])
    long_ascii_number_text = "Invoice 1234567890 paid on 2026-07-10. " * 1024
    long_arabic_text = "السلام عليكم ٠١٢٣٤٥٦٧٨٩ ي ك " * 1024
    numbers = tuple(index * 123_457 % 999_999_999_999_999 for index in range(2048))

    def convert_gregorian_dates_to_jalali() -> int:
        checksum = 0
        for item in gregorian_dates:
            converted = JalaliDate.to_jalali(item)
            checksum += converted.year + converted.month + converted.day
        return checksum

    def convert_jalali_dates_to_gregorian() -> int:
        checksum = 0
        for item in jalali_dates:
            converted = item.to_gregorian()
            checksum += converted.year + converted.month + converted.day
        return checksum

    def convert_gregorian_datetimes_to_jalali() -> int:
        checksum = 0
        for item in gregorian_datetimes:
            converted = JalaliDateTime.to_jalali(item)
            checksum += converted.year + converted.month + converted.day + converted.hour
        return checksum

    def format_jalali_datetimes() -> int:
        checksum = 0
        for item in jalali_datetimes:
            checksum += len(item.strftime("%Y-%m-%d %H:%M:%S.%f %z"))
        return checksum

    def parse_jalali_datetimes() -> int:
        checksum = 0
        for item in formatted_datetimes:
            parsed = JalaliDateTime.strptime(item, "%Y-%m-%d %H:%M:%S.%f %z")
            checksum += parsed.year + parsed.month + parsed.day + parsed.hour
        return checksum

    def translate_digits_and_characters() -> int:
        return len(digits.en_to_fa(long_ascii_number_text)) + len(characters.ar_to_fa(long_arabic_text))

    def convert_numbers_to_words() -> int:
        checksum = 0
        for item in numbers:
            checksum += len(digits.to_word(item))
        return checksum

    return (
        PerfCase("JalaliDate.to_jalali(date)", convert_gregorian_dates_to_jalali, len(gregorian_dates), 30.0),
        PerfCase("JalaliDate.to_gregorian()", convert_jalali_dates_to_gregorian, len(jalali_dates), 30.0),
        PerfCase(
            "JalaliDateTime.to_jalali(datetime)",
            convert_gregorian_datetimes_to_jalali,
            len(gregorian_datetimes),
            40.0,
        ),
        PerfCase("JalaliDateTime.strftime()", format_jalali_datetimes, len(jalali_datetimes), 80.0),
        PerfCase("JalaliDateTime.strptime()", parse_jalali_datetimes, len(formatted_datetimes), 250.0),
        PerfCase("digit/character translation", translate_digits_and_characters, 2, 1_500.0),
        PerfCase("digits.to_word(int)", convert_numbers_to_words, len(numbers), 80.0),
    )


def test_core_api_performance_budgets():
    for case in _make_perf_cases():
        best, median = _measure(case)
        assert best <= case.max_us_per_op
        assert median <= case.max_us_per_op * 1.5
