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

"""Backported classes and functions."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import io
import pathlib
import sys
from typing import Optional


if sys.version_info >= (3, 11):
	from enum import StrEnum
else:
	from backports.strenum import StrEnum


class Path(pathlib.Path):
	"""
	Backported pathlib.Path functionality.

	Currently backports the newline argument From 3.13 read_text.
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
			if hasattr(io, "text_encoding"):
				encoding = io.text_encoding(encoding)
			with self.open(mode="r", encoding=encoding, errors=errors, newline=newline) as f:
				text = f.read()
		return text


__all__: list[str] = [
	"Path",
	"StrEnum",
]
