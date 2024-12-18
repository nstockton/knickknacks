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

# Future Modules:
from __future__ import annotations

# Built-in Modules:
from unittest import TestCase

# Knickknacks Modules:
from knickknacks import numbers


class TestNumbers(TestCase):
	def test_clamp(self) -> None:
		self.assertEqual(numbers.clamp(10, 5, 20), 10)
		self.assertEqual(numbers.clamp(4, 5, 20), 5)
		self.assertEqual(numbers.clamp(50, 5, 20), 20)

	def test_floatToFraction(self) -> None:
		self.assertEqual(numbers.floatToFraction(0.25), "1/4")
		self.assertEqual(numbers.floatToFraction(3.13), "313/100")
		self.assertEqual(numbers.floatToFraction(2), "2")

	def test_roundHalfAwayFromZero(self) -> None:
		self.assertEqual(numbers.roundHalfAwayFromZero(5.4), 5.0)
		self.assertEqual(numbers.roundHalfAwayFromZero(5.5), 6.0)
		self.assertEqual(numbers.roundHalfAwayFromZero(-5.4), -5.0)
		self.assertEqual(numbers.roundHalfAwayFromZero(-5.5), -6.0)
