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
from knickknacks import xml


class TestXML(TestCase):
	def test_escape_xml_string(self) -> None:
		original_string: str = "<one&two'\">three"
		expected_string: str = "&lt;one&amp;two'\"&gt;three"
		self.assertEqual(xml.escape_xml_string(original_string), expected_string)

	def test_get_xml_attributes(self) -> None:
		self.assertEqual(
			xml.get_xml_attributes('test1=value1 test2="value2" test3 /'),
			{"test1": "value1", "test2": "value2", "test3": None},
		)

	def test_unescape_xml_bytes(self) -> None:
		original_bytes: bytes = b"&lt;'\"one&amp;gt;two&gt;three&#35;four&#x5F;&#x5f;five&amp;#35;six"
		expected_bytes: bytes = b"<'\"one&gt;two>three#four__five&#35;six"
		self.assertEqual(xml.unescape_xml_bytes(original_bytes), expected_bytes)
