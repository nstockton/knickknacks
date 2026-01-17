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

"""Shared type definitions."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import re
import sys
from collections.abc import Mapping
from typing import Any, ParamSpec, TypeAlias, TypeVar, Union


if sys.version_info >= (3, 12):
	from typing import override
else:
	from typing_extensions import override
if sys.version_info >= (3, 11):
	from typing import Self
else:
	from typing_extensions import Self
# Literal from typing module has various issues in different Python versions, see:
# https://typing-extensions.readthedocs.io/en/latest/#Literal
if sys.version_info >= (3, 10, 1):
	from typing import Literal
else:
	from typing_extensions import Literal  # type: ignore[assignment] # NOQA: UP035


AnyMappingType: TypeAlias = Mapping[Any, Any]
BytesOrStrType = TypeVar("BytesOrStrType", bytes, str)
ReBytesMatchType: TypeAlias = re.Match[bytes] | None
ReBytesPatternType: TypeAlias = re.Pattern[bytes]
ReMatchType: TypeAlias = re.Match[str] | None
RePatternType: TypeAlias = re.Pattern[str]


__all__: list[str] = [
	"AnyMappingType",
	"BytesOrStrType",
	"Literal",
	"ParamSpec",
	"ReBytesMatchType",
	"ReBytesPatternType",
	"ReMatchType",
	"RePatternType",
	"Self",
	"TypeAlias",
	"override",
]
