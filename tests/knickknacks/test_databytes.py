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
from knickknacks import databytes


class TestDataBytes(TestCase):
	def test_decodeBytes(self) -> None:
		asciiChars: str = "".join(chr(i) for i in range(128))
		latinChars: str = "".join(chr(i) for i in range(128, 256))
		latinReplacements: str = "".join(
			databytes.LATIN_DECODING_REPLACEMENTS.get(ord(char), "?") for char in latinChars
		)
		self.assertEqual(databytes.decodeBytes(bytes(asciiChars, "us-ascii")), asciiChars)
		self.assertEqual(databytes.decodeBytes(bytes(latinChars, "latin-1")), latinReplacements)
		self.assertEqual(databytes.decodeBytes(bytes(latinChars, "utf-8")), latinReplacements)

	def test_iterBytes(self) -> None:
		sent: bytes = b"hello"
		expected: tuple[bytes, ...] = (b"h", b"e", b"l", b"l", b"o")
		self.assertEqual(tuple(databytes.iterBytes(sent)), expected)

	def test_latin2ascii(self) -> None:
		with self.assertRaises(NotImplementedError):
			databytes.latin2ascii(UnicodeError("junk"))
