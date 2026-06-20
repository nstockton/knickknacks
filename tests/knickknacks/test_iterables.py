# Copyright (C) 2026 Nick Stockton
# SPDX-License-Identifier: MIT
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

	def test_human_sort(self) -> None:
		expected_output: list[str] = [str(i) for i in range(1, 1001)]
		badly_sorted: list[str] = sorted(expected_output)
		self.assertEqual(badly_sorted[:4], ["1", "10", "100", "1000"])
		self.assertEqual(iterables.human_sort(badly_sorted), expected_output)

	def test_lpad_list(self) -> None:
		lst: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		padding: int = 0
		# Non-fixed padding with 0's on the left.
		# Returned list will be of length greater than or equal to *count*.
		self.assertEqual(iterables.lpad_list([], padding, count=12, fixed=False), [0] * 12)
		self.assertEqual(iterables.lpad_list(lst, padding, count=12, fixed=False), [0] * 3 + lst)
		self.assertEqual(iterables.lpad_list(lst, padding, count=5, fixed=False), lst)
		# Fixed padding with 0's on the left.
		# Returned list will be of length equal to *count*.
		self.assertEqual(iterables.lpad_list([], padding, count=12, fixed=True), [0] * 12)
		self.assertEqual(iterables.lpad_list(lst, padding, count=12, fixed=True), [0] * 3 + lst)
		self.assertEqual(iterables.lpad_list(lst, padding, count=5, fixed=True), lst[:5])

	def test_pad_list(self) -> None:
		lst: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		padding: int = 0
		# Non-fixed padding with 0's on the right.
		# Returned list will be of length greater than or equal to *count*.
		self.assertEqual(iterables.pad_list([], padding, count=12, fixed=False), [0] * 12)
		self.assertEqual(iterables.pad_list(lst, padding, count=12, fixed=False), lst + [0] * 3)
		self.assertEqual(iterables.pad_list(lst, padding, count=5, fixed=False), lst)
		# Fixed padding with 0's on the right.
		# Returned list will be of length equal to *count*.
		self.assertEqual(iterables.pad_list([], padding, count=12, fixed=True), [0] * 12)
		self.assertEqual(iterables.pad_list(lst, padding, count=12, fixed=True), lst + [0] * 3)
		self.assertEqual(iterables.pad_list(lst, padding, count=5, fixed=True), lst[:5])


class TestFindAny(TestCase):
	"""Tests for iterables.find_any."""

	def test_empty_values_returns_zero(self) -> None:
		self.assertEqual(iterables.find_any([1, 2, 3], []), 0)
		self.assertEqual(iterables.find_any([], []), 0)
		self.assertEqual(iterables.find_any("abc", ""), 0)  # Empty str is falsy.
		self.assertEqual(iterables.find_any(b"abc", b""), 0)  # Empty bytes is falsy.

	def test_empty_sequence_returns_minus_one(self) -> None:
		self.assertEqual(iterables.find_any([], [1, 2, 3]), -1)
		self.assertEqual(iterables.find_any("", "xyz"), -1)
		self.assertEqual(iterables.find_any(b"", [97]), -1)  # Bytes sequence.

	def test_no_match_returns_minus_one(self) -> None:
		self.assertEqual(iterables.find_any([1, 2, 3], [4, 5, 6]), -1)
		self.assertEqual(iterables.find_any("hello", "xyz"), -1)
		self.assertEqual(iterables.find_any(b"hello", b"xyz"), -1)  # Integers not present.

	def test_first_occurrence_of_any_value(self) -> None:
		self.assertEqual(iterables.find_any([1, 2, 3, 2], [2, 4]), 1)
		self.assertEqual(iterables.find_any("abcde", "ce"), 2)  # 'c' appears before 'e'.
		self.assertEqual(iterables.find_any("hello", "lo"), 2)  # 'l' first.

	def test_various_sequence_types(self) -> None:
		self.assertEqual(iterables.find_any((10, 20, 30), [20]), 1)  # Tuple.
		self.assertEqual(iterables.find_any("python", {"y", "t"}), 1)  # String + set.
		# Bytes elements are ints; values must be ints.
		self.assertEqual(iterables.find_any(b"data", [97]), 1)  # 'a' is 97 in ASCII.

	def test_various_values_iterables(self) -> None:
		self.assertEqual(iterables.find_any([1, 2, 3], (2, 4)), 1)
		self.assertEqual(iterables.find_any(["a", "b", "c"], {"b"}), 1)


class TestRFindAny(TestCase):
	"""Tests for iterables.rfind_any."""

	def test_empty_values_returns_length(self) -> None:
		self.assertEqual(iterables.rfind_any([1, 2, 3], []), 3)
		self.assertEqual(iterables.rfind_any([], []), 0)
		self.assertEqual(iterables.rfind_any("abc", ""), 3)  # Empty str is falsy.
		self.assertEqual(iterables.rfind_any(b"abc", b""), 3)  # Empty bytes is falsy.

	def test_empty_sequence_returns_minus_one(self) -> None:
		self.assertEqual(iterables.rfind_any([], [1, 2, 3]), -1)
		self.assertEqual(iterables.rfind_any("", "xyz"), -1)
		self.assertEqual(iterables.rfind_any(b"", [97]), -1)  # Bytes sequence.

	def test_no_match_returns_minus_one(self) -> None:
		self.assertEqual(iterables.rfind_any([1, 2, 3], [4, 5, 6]), -1)
		self.assertEqual(iterables.rfind_any("hello", "xyz"), -1)
		self.assertEqual(iterables.rfind_any(b"hello", b"xyz"), -1)  # Integers not present.

	def test_last_occurrence_of_any_value(self) -> None:
		self.assertEqual(iterables.rfind_any([2, 1, 2, 3], [2, 4]), 2)
		self.assertEqual(iterables.rfind_any("abcde", "cd"), 3)  # 'd' appears after 'c'.
		self.assertEqual(iterables.rfind_any("hello", "el"), 3)  # 'l' last.

	def test_various_sequence_types(self) -> None:
		self.assertEqual(iterables.rfind_any((10, 20, 30), [20]), 1)  # Tuple.
		self.assertEqual(iterables.rfind_any("python", {"y", "t"}), 2)  # String + set.
		# Bytes elements are ints; values must be ints.
		self.assertEqual(iterables.rfind_any(b"data", [97]), 3)  # 'a' is 97 in ASCII.

	def test_various_values_iterables(self) -> None:
		self.assertEqual(iterables.rfind_any([1, 2, 3], (2, 4)), 1)
		self.assertEqual(iterables.rfind_any(["a", "b", "c"], {"b"}), 1)
