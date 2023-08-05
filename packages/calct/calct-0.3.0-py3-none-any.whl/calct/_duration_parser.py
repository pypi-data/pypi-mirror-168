#   calct: Easily do calculations on hours and minutes using the command line
#   Copyright (C) 2022  Philippe Warren
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import re
from typing import NamedTuple

from calct._common import Number


def _parse_hours(time_str: str) -> Number:
    try:
        hours_int = int(time_str)
        return hours_int
    except ValueError:
        try:
            hours_float = float(time_str)
            return hours_float
        except ValueError as ex:
            raise ValueError(f"Invalid hours: {time_str}") from ex


def _parse_minutes(time_str: str) -> int:
    try:
        minutes_int = int(time_str)
        return minutes_int
    except ValueError as ex:
        raise ValueError(f"Invalid minutes: {time_str}") from ex


class Time(NamedTuple):
    """A tuple of hours and minutes."""

    hours: Number
    minutes: int


DurationMatcher = re.Pattern[str]


def compile_matcher(matcher: str) -> DurationMatcher:
    float_pattern = r"(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?"
    int_pattern = r"\d+"
    matcher_re = (
        "^" + matcher.replace("%H", rf"(?P<hours>{float_pattern})").replace("%M", rf"(?P<minutes>{int_pattern})") + "$"
    )
    return re.compile(matcher_re, re.VERBOSE)


def parse_duration(time_str: str, pattern: DurationMatcher) -> Time:
    matches = pattern.match(time_str)
    if matches is None:
        raise ValueError(f"Invalid duration: {time_str}")
    matches_dict = {"hours": "0", "minutes": "0"} | matches.groupdict()
    return Time(hours=_parse_hours(matches_dict["hours"]), minutes=_parse_minutes(matches_dict["minutes"]))
