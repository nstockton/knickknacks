# Copyright (c) 2025 Nick Stockton
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# -----------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# -----------------------------------------------------------------------------
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Stuff to do with numbers."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import fractions
import math


def clamp(value: float, minimum: float, maximum: float) -> float:
	"""
	Clamp a value to be between minimum and maximum.

	Args:
		value: Value to clamp.
		minimum: Lower limit.
		maximum: Upper limit.

	Returns:
		Clamped value.
	"""
	return max(minimum, min(value, maximum))


def float_to_fraction(number: float) -> str:
	"""
	Converts a float to a fraction.

	Note:
		https://stackoverflow.com/questions/23344185/how-to-convert-a-decimal-number-into-fraction

	Args:
		number: The number to convert.

	Returns:
		A string containing the number as a fraction.
	"""
	return str(fractions.Fraction(number).limit_denominator())


def round_half_away_from_zero(number: float, decimals: int = 0) -> float:
	"""
	Rounds a float away from 0 if the fractional is 5 or more.

	Note:
		https://realpython.com/python-rounding

	Args:
		number: The number to round.
		decimals: The number of fractional decimal places to round to.

	Returns:
		The number after rounding.
	"""
	multiplier = 10**decimals
	return math.copysign(math.floor(abs(number) * multiplier + 0.5) / multiplier, number)
