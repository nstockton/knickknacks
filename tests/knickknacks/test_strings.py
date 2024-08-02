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
from collections.abc import Callable
from unittest import TestCase

# Knickknacks Modules:
from knickknacks import strings


class TestStrings(TestCase):
	def test_camelCase(self) -> None:
		self.assertEqual(strings.camelCase("", "_"), "")
		self.assertEqual(strings.camelCase("this_is_a_test", "_"), "thisIsATest")

	def test_formatDocString(self) -> None:
		docString: str = (
			"\nTest Doc String\n"
			+ "This is the first line below the title.\n"
			+ "\tThis is an indented line below the first. "
			+ "Let's make it long so we can check if word wrapping works.\n"
			+ "This is the final line, which should be at indention level 0.\n"
		)
		expectedOutput: str = (
			"Test Doc String\n"
			+ "This is the first line below the title.\n"
			+ "\tThis is an indented line below the first. Let's make it long so we can check\n"
			+ "\tif word wrapping works.\n"
			+ "This is the final line, which should be at indention level 0."
		)
		testFunction: Callable[[], None] = lambda: None  # NOQA: E731
		testFunction.__doc__ = docString
		expectedOutputIndentTwoSpace: str = "\n".join(
			"  " + line.replace("\t", "  ") for line in expectedOutput.splitlines()
		)
		width: int = 79
		self.assertEqual(strings.formatDocString(docString, width), expectedOutput)
		self.assertEqual(strings.formatDocString(docString, width, prefix=""), expectedOutput)
		self.assertEqual(strings.formatDocString(docString, width, prefix="  "), expectedOutputIndentTwoSpace)
		self.assertEqual(strings.formatDocString(testFunction, width), expectedOutput)
		self.assertEqual(strings.formatDocString(testFunction, width, prefix=""), expectedOutput)
		self.assertEqual(
			strings.formatDocString(testFunction, width, prefix="  "), expectedOutputIndentTwoSpace
		)

	def test_minIndent(self) -> None:
		self.assertEqual(strings.minIndent("hello\nworld"), "")
		self.assertEqual(strings.minIndent("\thello\n\t\tworld"), "\t")

	def test_multiReplace(self) -> None:
		replacements: tuple[tuple[str, str], ...] = (("ll", "yy"), ("h", "x"), ("o", "z"))
		text: str = "hello world"
		expectedOutput: str = "xeyyz wzrld"
		self.assertEqual(strings.multiReplace(text, replacements), expectedOutput)
		self.assertEqual(strings.multiReplace(text, ()), text)

	def test_regexFuzzy(self) -> None:
		with self.assertRaises(TypeError):
			strings.regexFuzzy(None)  # type: ignore[arg-type]
		self.assertEqual(strings.regexFuzzy(""), "")
		self.assertEqual(strings.regexFuzzy([]), "")
		self.assertEqual(strings.regexFuzzy([""]), "")
		self.assertEqual(strings.regexFuzzy(["", ""]), "|")
		self.assertEqual(strings.regexFuzzy("east"), "e(a(s(t)?)?)?")
		self.assertEqual(strings.regexFuzzy(["east"]), "e(a(s(t)?)?)?")
		self.assertEqual(strings.regexFuzzy(("east")), "e(a(s(t)?)?)?")
		expectedOutput: str = "e(a(s(t)?)?)?|w(e(s(t)?)?)?"
		self.assertEqual(strings.regexFuzzy(["east", "west"]), expectedOutput)
		self.assertEqual(strings.regexFuzzy(("east", "west")), expectedOutput)

	def test_removePrefix(self) -> None:
		self.assertEqual(strings.removePrefix("hello", "he"), "llo")
		self.assertEqual(strings.removePrefix("hello", "xx"), "hello")
		self.assertEqual(strings.removePrefix("hello", ""), "hello")

	def test_removeSuffix(self) -> None:
		self.assertEqual(strings.removeSuffix("hello", "lo"), "hel")
		self.assertEqual(strings.removeSuffix("hello", "xx"), "hello")
		self.assertEqual(strings.removeSuffix("hello", ""), "hello")

	def test_stripAnsi(self) -> None:
		sent: str = "\x1b[32mhello\x1b[0m"
		expected: str = "hello"
		self.assertEqual(strings.stripAnsi(sent), expected)

	def test_simplified(self) -> None:
		sent: str = "Hello world\r\nThis  is\ta\r\n\r\ntest."
		expected: str = "Hello world This is a test."
		self.assertEqual(strings.simplified(sent), expected)
