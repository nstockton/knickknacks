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

"""Shared type definitions."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import sys
from re import Match, Pattern
from typing import TypeVar, Union


if sys.version_info >= (3, 12):
	from typing import override
else:
	from typing_extensions import override
if sys.version_info >= (3, 11):
	from typing import Self
else:
	from typing_extensions import Self
if sys.version_info >= (3, 10):
	from typing import TypeAlias
else:
	from typing_extensions import TypeAlias
# Literal from typing module has various issues in different Python versions, see:
# https://typing-extensions.readthedocs.io/en/latest/#Literal
if sys.version_info >= (3, 10, 1) or (3, 9, 8) <= sys.version_info < (3, 10):
	from typing import Literal
else:
	from typing_extensions import Literal  # type: ignore[assignment]


BytesOrStr = TypeVar("BytesOrStr", bytes, str)
REGEX_MATCH: TypeAlias = Union[Match[str], None]
REGEX_PATTERN: TypeAlias = Pattern[str]
REGEX_BYTES_MATCH: TypeAlias = Union[Match[bytes], None]
REGEX_BYTES_PATTERN: TypeAlias = Pattern[bytes]


__all__: list[str] = [
	"BytesOrStr",
	"REGEX_MATCH",
	"REGEX_PATTERN",
	"REGEX_BYTES_MATCH",
	"REGEX_BYTES_PATTERN",
]
