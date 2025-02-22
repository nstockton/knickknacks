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

# Future Modules:
from __future__ import annotations

# Built-in Modules:
from unittest import TestCase

# Knickknacks Modules:
from knickknacks import databytes


class TestDataBytes(TestCase):
	def test_decode_bytes(self) -> None:
		ascii_chars: str = "".join(chr(i) for i in range(128))
		latin_chars: str = "".join(chr(i) for i in range(128, 256))
		latin_replacements: str = "".join(
			databytes.LATIN_DECODING_REPLACEMENTS.get(ord(char), "?") for char in latin_chars
		)
		self.assertEqual(databytes.decode_bytes(bytes(ascii_chars, "us-ascii")), ascii_chars)
		self.assertEqual(databytes.decode_bytes(bytes(latin_chars, "latin-1")), latin_replacements)
		self.assertEqual(databytes.decode_bytes(bytes(latin_chars, "utf-8")), latin_replacements)

	def test_iter_bytes(self) -> None:
		sent: bytes = b"hello"
		expected: tuple[bytes, ...] = (b"h", b"e", b"l", b"l", b"o")
		self.assertEqual(tuple(databytes.iter_bytes(sent)), expected)

	def test_latin_to_ascii(self) -> None:
		with self.assertRaises(NotImplementedError):
			databytes._latin_to_ascii(UnicodeError("junk"))  # NOQA: SLF001
