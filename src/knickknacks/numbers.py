# Copyright (c) 2024 Nick Stockton
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
	Clamps the given value between the given minimum and maximum values.

	Args:
		value: The value to restrict inside the range defined by minimum and maximum.
		minimum: The minimum value to compare against.
		maximum: The maximum value to compare against.

	Returns:
		The result between minimum and maximum.
	"""
	return minimum if value < minimum else maximum if value > maximum else value


def floatToFraction(number: float) -> str:
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


def roundHalfAwayFromZero(number: float, decimals: int = 0) -> float:
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
