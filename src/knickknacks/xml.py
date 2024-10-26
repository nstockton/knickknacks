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

"""Stuff to do with XML."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import re
from typing import Union

# Local Modules:
from .strings import multiReplace
from .typedef import ReBytesPatternType, RePatternType


ESCAPE_XML_STR_ENTITIES: tuple[tuple[str, str], ...] = (
	("&", "&amp;"),  # & must always be first when escaping.
	("<", "&lt;"),
	(">", "&gt;"),
)
UNESCAPE_XML_STR_ENTITIES: tuple[tuple[str, str], ...] = tuple(
	reversed(  # &amp; must always be last when unescaping.
		tuple((second, first) for first, second in ESCAPE_XML_STR_ENTITIES)
	)
)

ESCAPE_XML_BYTES_ENTITIES: tuple[tuple[bytes, bytes], ...] = tuple(
	(bytes(first, "us-ascii"), bytes(second, "us-ascii")) for first, second in ESCAPE_XML_STR_ENTITIES
)
UNESCAPE_XML_BYTES_ENTITIES: tuple[tuple[bytes, bytes], ...] = tuple(
	(bytes(first, "us-ascii"), bytes(second, "us-ascii")) for first, second in UNESCAPE_XML_STR_ENTITIES
)

UNESCAPE_XML_NUMERIC_BYTES_REGEX: ReBytesPatternType = re.compile(rb"&#(?P<hex>x?)(?P<value>[0-9a-zA-Z]+);")
XML_ATTRIBUTE_REGEX: RePatternType = re.compile(r"([\w-]+)(\s*=+\s*('[^']*'|\"[^\"]*\"|(?!['\"])[^\s]*))?")


def escapeXMLString(text: str) -> str:
	"""
	Escapes XML entities in a string.

	Args:
		text: The string to escape.

	Returns:
		A copy of the string with XML entities escaped.
	"""
	return multiReplace(text, ESCAPE_XML_STR_ENTITIES)


def getXMLAttributes(text: str) -> dict[str, Union[str, None]]:
	"""
	Extracts XML attributes from a tag.

	The supplied string must only contain attributes, not the tag name.

	Note:
		Adapted from the html.parser module of the Python standard library.

	Args:
		text: The text to be parsed.

	Returns:
		The extracted attributes.
	"""
	attributes: dict[str, Union[str, None]] = {}
	for name, rest, value in XML_ATTRIBUTE_REGEX.findall(text):
		if not rest:
			attributes[name.lower()] = None
		elif value[:1] == "'" == value[-1:] or value[:1] == '"' == value[-1:]:
			# The value is enclosed in single or double quotes.
			attributes[name.lower()] = value[1:-1]  # Strip the quotes from beginning and end.
		else:
			attributes[name.lower()] = value
	return attributes


def unescapeXMLBytes(data: bytes) -> bytes:
	"""
	Unescapes XML entities in a bytes-like object.

	Args:
		data: The data to unescape.

	Returns:
		A copy of the data with XML entities unescaped.
	"""

	def referenceToBytes(match: re.Match[bytes]) -> bytes:
		isHex: bytes = match.group("hex")
		value: bytes = match.group("value")
		return bytes((int(value, 16 if isHex else 10),))

	return multiReplace(
		UNESCAPE_XML_NUMERIC_BYTES_REGEX.sub(referenceToBytes, data), UNESCAPE_XML_BYTES_ENTITIES
	)
