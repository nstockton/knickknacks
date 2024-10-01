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
import re
import statistics
from collections.abc import Iterable, Sequence
from typing import Any


def average(items: Iterable[float]) -> float:
	"""
	Calculates the average item length of an iterable.

	Args:
		items: The iterable of items.

	Returns:
		The average item length.
	"""
	try:
		return statistics.mean(items)
	except statistics.StatisticsError:
		# No items.
		return 0


def humanSort(lst: Sequence[str]) -> list[str]:
	"""
	Sorts a list of strings, with numbers sorted according to their numeric value.

	Args:
		lst: The list of strings to be sorted.

	Returns:
		The items of the list, with strings containing numbers sorted according to their numeric value.
	"""
	return sorted(
		lst,
		key=lambda item: [
			int(text) if text.isdigit() else text for text in re.split(r"(\d+)", item, flags=re.UNICODE)
		],
	)


def lpadList(lst: Sequence[Any], padding: Any, count: int, fixed: bool = False) -> list[Any]:
	"""
	Pad the left side of a list.

	Args:
		lst: The list to be padded.
		padding: The item to use for padding.
		count: The minimum size of the returned list.
		fixed: True if the maximum size of the returned list should be restricted to count, False otherwise.

	Returns:
		A padded copy of the list.
	"""
	if fixed:
		return [*[padding] * (count - len(lst)), *lst][:count]
	else:
		return [*[padding] * (count - len(lst)), *lst]


def padList(lst: Sequence[Any], padding: Any, count: int, fixed: bool = False) -> list[Any]:
	"""
	Pad the right side of a list.

	Args:
		lst: The list to be padded.
		padding: The item to use for padding.
		count: The minimum size of the returned list.
		fixed: True if the maximum size of the returned list should be restricted to count, False otherwise.

	Returns:
		A padded copy of the list.
	"""
	if fixed:
		return [*lst, *[padding] * (count - len(lst))][:count]
	else:
		return [*lst, *[padding] * (count - len(lst))]
