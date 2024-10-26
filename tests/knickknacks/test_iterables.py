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
from knickknacks import iterables


class TestIterables(TestCase):
	def test_average(self) -> None:
		self.assertEqual(iterables.average(range(7)), 3)
		self.assertEqual(iterables.average([]), 0)

	def test_humanSort(self) -> None:
		expectedOutput: list[str] = [str(i) for i in range(1, 1001)]
		badlySorted: list[str] = sorted(expectedOutput)
		self.assertEqual(badlySorted[:4], ["1", "10", "100", "1000"])
		self.assertEqual(iterables.humanSort(badlySorted), expectedOutput)

	def test_lpadList(self) -> None:
		lst: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		padding: int = 0
		# Non-fixed padding with 0's on the left.
		# Returned list will be of length greater than or equal to *count*.
		self.assertEqual(iterables.lpadList([], padding, count=12, fixed=False), [0] * 12)
		self.assertEqual(iterables.lpadList(lst, padding, count=12, fixed=False), [0] * 3 + lst)
		self.assertEqual(iterables.lpadList(lst, padding, count=5, fixed=False), lst)
		# Fixed padding with 0's on the left.
		# Returned list will be of length equal to *count*.
		self.assertEqual(iterables.lpadList([], padding, count=12, fixed=True), [0] * 12)
		self.assertEqual(iterables.lpadList(lst, padding, count=12, fixed=True), [0] * 3 + lst)
		self.assertEqual(iterables.lpadList(lst, padding, count=5, fixed=True), lst[:5])

	def test_padList(self) -> None:
		lst: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		padding: int = 0
		# Non-fixed padding with 0's on the right.
		# Returned list will be of length greater than or equal to *count*.
		self.assertEqual(iterables.padList([], padding, count=12, fixed=False), [0] * 12)
		self.assertEqual(iterables.padList(lst, padding, count=12, fixed=False), lst + [0] * 3)
		self.assertEqual(iterables.padList(lst, padding, count=5, fixed=False), lst)
		# Fixed padding with 0's on the right.
		# Returned list will be of length equal to *count*.
		self.assertEqual(iterables.padList([], padding, count=12, fixed=True), [0] * 12)
		self.assertEqual(iterables.padList(lst, padding, count=12, fixed=True), lst + [0] * 3)
		self.assertEqual(iterables.padList(lst, padding, count=5, fixed=True), lst[:5])
