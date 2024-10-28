# Copyright (C) 2024 Nick Stockton
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Backported classes and functions."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import enum
import io
import pathlib
import sys
from typing import Optional, Self


class Path(pathlib.Path):
	"""
	Backported pathlib.Path functionality.

	Currently backports the newline argument From 3.13 read_text, and 3.10 write_text.
	"""

	def read_text(
		self, encoding: Optional[str] = None, errors: Optional[str] = None, newline: Optional[str] = None
	) -> str:
		"""
		Open the file in text mode, read it, and close the file.

		Args:
			encoding: The character encoding to use.
			errors: How encoding errors should be handled.
			newline: How newlines should be handled.

		Returns:
			The contents of the file.
		"""
		if sys.version_info >= (3, 13):
			text = super().read_text(encoding, errors, newline)
		else:
			encoding = io.text_encoding(encoding)
			with self.open(mode="r", encoding=encoding, errors=errors, newline=newline) as f:
				text = f.read()
		return text

	def write_text(
		self,
		data: str,
		encoding: Optional[str] = None,
		errors: Optional[str] = None,
		newline: Optional[str] = None,
	) -> int:
		"""
		Open the file in text mode, write to it, and close the file.

		Args:
			data: The data to be written.
			encoding: The character encoding to use.
			errors: How encoding errors should be handled.
			newline: How newlines should be handled.

		Returns:
			The number of bytes written.

		Raises:
			TypeError: Data is not an instance of `str`.
		"""
		if sys.version_info >= (3, 10):
			num_written = super().write_text(data, encoding, errors, newline)
		else:
			if not isinstance(data, str):  # type: ignore[unreachable]
				raise TypeError(f"data must be str, not {data.__class__.__name__}")
			encoding = io.text_encoding(encoding)
			with self.open(mode="w", encoding=encoding, errors=errors, newline=newline) as f:
				num_written = f.write(data)
		return num_written


class StrEnumBackport(str, enum.Enum):
	"""
	An Enum where members are also (and must be) strings.

	Backported from Python 3.11.
	"""

	def __str__(self) -> str:
		return str(self.value)

	def __new__(cls: type[Self], *values: str) -> Self:
		if len(values) > 3:
			raise TypeError(f"too many arguments for str(): {values!r}")
		if len(values) == 1 and not isinstance(values[0], str):
			raise TypeError(f"{values[0]!r} is not a string")
		if len(values) >= 2 and not isinstance(values[1], str):
			raise TypeError(f"encoding must be a string, not {values[1]!r}")
		if len(values) == 3 and not isinstance(values[2], str):
			raise TypeError(f"errors must be a string, not {values[2]!r}")
		value = str(*values)
		member = str.__new__(cls, value)
		member._value_ = value
		return member

	@staticmethod
	def _generate_next_value_(name: str, start: int, count: int, last_values: list[str]) -> str:
		"""
		Retrieves the lower-cased version of the member name.

		Returns:
			The member name, in lower-case.
		"""
		return name.lower()


StrEnum = enum.StrEnum if sys.version_info >= (3, 11) else StrEnumBackport


__all__: list[str] = [
	"Path",
	"StrEnum",
]
