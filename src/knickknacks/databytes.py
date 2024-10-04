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
import codecs
from collections.abc import Generator
from contextlib import suppress
from typing import Union


# Latin-1 replacement values taken from the MUME help page.
# https://mume.org/help/latin1
LATIN_ENCODING_REPLACEMENTS: dict[str, bytes] = {
	"\u00a0": b" ",
	"\u00a1": b"!",
	"\u00a2": b"c",
	"\u00a3": b"L",
	"\u00a4": b"$",
	"\u00a5": b"Y",
	"\u00a6": b"|",
	"\u00a7": b"P",
	"\u00a8": b'"',
	"\u00a9": b"C",
	"\u00aa": b"a",
	"\u00ab": b"<",
	"\u00ac": b",",
	"\u00ad": b"-",
	"\u00ae": b"R",
	"\u00af": b"-",
	"\u00b0": b"d",
	"\u00b1": b"+",
	"\u00b2": b"2",
	"\u00b3": b"3",
	"\u00b4": b"'",
	"\u00b5": b"u",
	"\u00b6": b"P",
	"\u00b7": b"*",
	"\u00b8": b",",
	"\u00b9": b"1",
	"\u00ba": b"o",
	"\u00bb": b">",
	"\u00bc": b"4",
	"\u00bd": b"2",
	"\u00be": b"3",
	"\u00bf": b"?",
	"\u00c0": b"A",
	"\u00c1": b"A",
	"\u00c2": b"A",
	"\u00c3": b"A",
	"\u00c4": b"A",
	"\u00c5": b"A",
	"\u00c6": b"A",
	"\u00c7": b"C",
	"\u00c8": b"E",
	"\u00c9": b"E",
	"\u00ca": b"E",
	"\u00cb": b"E",
	"\u00cc": b"I",
	"\u00cd": b"I",
	"\u00ce": b"I",
	"\u00cf": b"I",
	"\u00d0": b"D",
	"\u00d1": b"N",
	"\u00d2": b"O",
	"\u00d3": b"O",
	"\u00d4": b"O",
	"\u00d5": b"O",
	"\u00d6": b"O",
	"\u00d7": b"*",
	"\u00d8": b"O",
	"\u00d9": b"U",
	"\u00da": b"U",
	"\u00db": b"U",
	"\u00dc": b"U",
	"\u00dd": b"Y",
	"\u00de": b"T",
	"\u00df": b"s",
	"\u00e0": b"a",
	"\u00e1": b"a",
	"\u00e2": b"a",
	"\u00e3": b"a",
	"\u00e4": b"a",
	"\u00e5": b"a",
	"\u00e6": b"a",
	"\u00e7": b"c",
	"\u00e8": b"e",
	"\u00e9": b"e",
	"\u00ea": b"e",
	"\u00eb": b"e",
	"\u00ec": b"i",
	"\u00ed": b"i",
	"\u00ee": b"i",
	"\u00ef": b"i",
	"\u00f0": b"d",
	"\u00f1": b"n",
	"\u00f2": b"o",
	"\u00f3": b"o",
	"\u00f4": b"o",
	"\u00f5": b"o",
	"\u00f6": b"o",
	"\u00f7": b"/",
	"\u00f8": b"o",
	"\u00f9": b"u",
	"\u00fa": b"u",
	"\u00fb": b"u",
	"\u00fc": b"u",
	"\u00fd": b"y",
	"\u00fe": b"t",
	"\u00ff": b"y",
}
LATIN_DECODING_REPLACEMENTS: dict[int, str] = {
	ord(k): str(v, "us-ascii") for k, v in LATIN_ENCODING_REPLACEMENTS.items()
}


def decodeBytes(data: bytes) -> str:
	"""
	Decodes bytes into a string.

	If data contains Latin-1 characters, they will be replaced with ASCII equivalents.

	Args:
		data: The data to be decoded.

	Returns:
		The decoded string.
	"""
	# Try to decode ASCII first, for speed.
	with suppress(UnicodeDecodeError):
		return str(data, "us-ascii")
	# Translate non-ASCII characters to their ASCII equivalents.
	try:
		# If encoded UTF-8, re-encode the data before decoding because of multi-byte code points.
		return data.decode("utf-8").encode("us-ascii", "latin2ascii").decode("us-ascii")
	except UnicodeDecodeError:
		# Assume data is encoded Latin-1.
		return str(data, "us-ascii", "latin2ascii")


def iterBytes(data: bytes) -> Generator[bytes, None, None]:
	"""
	A generator which yields each byte of a bytes-like object.

	Args:
		data: The data to process.

	Yields:
		Each byte of data as a bytes object.
	"""
	for i in range(len(data)):
		yield data[i : i + 1]


def latin2ascii(error: UnicodeError) -> tuple[Union[bytes, str], int]:
	if isinstance(error, UnicodeEncodeError):
		# Return value can be bytes or a string.
		return LATIN_ENCODING_REPLACEMENTS.get(error.object[error.start], b"?"), error.start + 1
	if isinstance(error, UnicodeDecodeError):
		# Return value must be a string.
		return LATIN_DECODING_REPLACEMENTS.get(error.object[error.start], "?"), error.start + 1
	# Probably UnicodeTranslateError.
	raise NotImplementedError("How'd you manage this?") from error


codecs.register_error("latin2ascii", latin2ascii)
