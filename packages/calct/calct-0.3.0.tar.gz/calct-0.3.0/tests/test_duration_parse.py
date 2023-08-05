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

import pytest

from calct.duration import Duration


def test_duration_parse_h():
    assert Duration.parse("3h") == Duration(hours=3)


def test_duration_parse_h_min():
    assert Duration.parse("3h12") == Duration(hours=3, minutes=12)


def test_duration_parse_colon():
    assert Duration.parse("3:12") == Duration(hours=3, minutes=12)


def test_duration_parse_min():
    assert Duration.parse("56m") == Duration(minutes=56)


def test_duration_parse_min_bigger_than_59():
    assert Duration.parse("86m") == Duration(minutes=86)


def test_duration_parse_h_bigger_than_23():
    assert Duration.parse("32h12") == Duration(hours=32, minutes=12)


def test_duration_parse_decimal_hours():
    assert Duration.parse("3.5h") == Duration(hours=3.5)
    assert Duration.parse(".5h12") == Duration(hours=0.5, minutes=12)


def test_duration_parse_empty():
    with pytest.raises(ValueError):
        Duration.parse("")


def test_duration_parse_exponential_hours():
    assert Duration.parse(".5e2h12") == Duration(hours=0.5e2, minutes=12)
    assert Duration.parse("3E2h12") == Duration(hours=3e2, minutes=12)
    assert Duration.parse("1000e-1h12") == Duration(hours=1000e-1, minutes=12)
    assert Duration.parse("123.34e-3h12") == Duration(hours=123.34e-3, minutes=12)
    assert Duration.parse("123.34e+3h12") == Duration(hours=123.34e3, minutes=12)


def test_duration_parse_float_minutes():
    with pytest.raises(ValueError):
        Duration.parse("3.5m")
    with pytest.raises(ValueError):
        Duration.parse(".5m")
    with pytest.raises(ValueError):
        Duration.parse(":.5")
    with pytest.raises(ValueError):
        Duration.parse("h4e-2")


def test_duration_parse_pure_number():
    with pytest.raises(ValueError):
        Duration.parse("3")
