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
from collections.abc import Callable
from unittest import TestCase

# Knickknacks Modules:
from knickknacks import strings


class TestStrings(TestCase):
	def test_camel_case(self) -> None:
		self.assertEqual(strings.camel_case("", "_"), "")
		self.assertEqual(strings.camel_case("this_is_a_test", "_"), "thisIsATest")

	def test_format_docstring(self) -> None:
		docstring: str = (
			"\nTest Doc String\n"
			+ "This is the first line below the title.\n"
			+ "\tThis is an indented line below the first. "
			+ "Let's make it long so we can check if word wrapping works.\n"
			+ "This is the final line, which should be at indention level 0.\n"
		)
		expected_output: str = (
			"Test Doc String\n"
			+ "This is the first line below the title.\n"
			+ "\tThis is an indented line below the first. Let's make it long so we can check\n"
			+ "\tif word wrapping works.\n"
			+ "This is the final line, which should be at indention level 0."
		)
		test_function: Callable[[], None] = lambda: None  # NOQA: E731
		test_function.__doc__ = docstring
		expected_output_indent_two_space: str = "\n".join(
			"  " + line.replace("\t", "  ") for line in expected_output.splitlines()
		)
		width: int = 79
		self.assertEqual(strings.format_docstring(docstring, width), expected_output)
		self.assertEqual(strings.format_docstring(docstring, width, prefix=""), expected_output)
		self.assertEqual(
			strings.format_docstring(docstring, width, prefix="  "), expected_output_indent_two_space
		)
		self.assertEqual(strings.format_docstring(test_function, width), expected_output)
		self.assertEqual(strings.format_docstring(test_function, width, prefix=""), expected_output)
		self.assertEqual(
			strings.format_docstring(test_function, width, prefix="  "), expected_output_indent_two_space
		)

	def test_has_white_space(self) -> None:
		should_be_true: str = "\tHello world\r\nThis  is\ta\r\n\r\ntest. "
		should_be_false: str = "HelloworldThisisatest."
		self.assertTrue(strings.has_white_space(should_be_true))
		self.assertFalse(strings.has_white_space(should_be_false))

	def test_has_white_space_except_space(self) -> None:
		should_be_true: str = "\tHello world\r\nThis  is\ta\r\n\r\ntest. "
		should_be_false: str = "Hello worldThis  isatest. "
		self.assertTrue(strings.has_white_space_except_space(should_be_true))
		self.assertFalse(strings.has_white_space_except_space(should_be_false))

	def test_min_indent(self) -> None:
		self.assertEqual(strings.min_indent("hello\nworld"), "")
		self.assertEqual(strings.min_indent("\thello\n\t\tworld"), "\t")

	def test_multi_replace(self) -> None:
		replacements: tuple[tuple[str, str], ...] = (("ll", "yy"), ("h", "x"), ("o", "z"))
		text: str = "hello world"
		expected_output: str = "xeyyz wzrld"
		self.assertEqual(strings.multi_replace(text, replacements), expected_output)
		self.assertEqual(strings.multi_replace(text, ()), text)

	def test_regex_fuzzy(self) -> None:
		with self.assertRaises(TypeError):
			strings.regex_fuzzy(None)  # type: ignore[arg-type]
		self.assertEqual(strings.regex_fuzzy(""), "")
		self.assertEqual(strings.regex_fuzzy([]), "")
		self.assertEqual(strings.regex_fuzzy([""]), "")
		self.assertEqual(strings.regex_fuzzy(["", ""]), "|")
		self.assertEqual(strings.regex_fuzzy("east"), "e(a(s(t)?)?)?")
		self.assertEqual(strings.regex_fuzzy(["east"]), "e(a(s(t)?)?)?")
		self.assertEqual(strings.regex_fuzzy("east"), "e(a(s(t)?)?)?")
		expected_output: str = "e(a(s(t)?)?)?|w(e(s(t)?)?)?"
		self.assertEqual(strings.regex_fuzzy(["east", "west"]), expected_output)
		self.assertEqual(strings.regex_fuzzy(("east", "west")), expected_output)

	def test_remove_white_space(self) -> None:
		sent: str = "\tHello world\r\nThis  is\ta\r\n\r\ntest. "
		expected: str = "HelloworldThisisatest."
		self.assertEqual(strings.remove_white_space(sent), expected)

	def test_remove_white_space_except_space(self) -> None:
		sent: str = "\tHello world\r\nThis  is\ta\r\n\r\ntest. "
		expected: str = "Hello worldThis  isatest. "
		self.assertEqual(strings.remove_white_space_except_space(sent), expected)

	def test_simplified(self) -> None:
		sent: str = "\tHello world\r\nThis  is\ta\r\n\r\ntest. "
		expected: str = "Hello world This is a test."
		self.assertEqual(strings.simplified(sent), expected)

	def test_strip_ansi(self) -> None:
		sent: str = "\x1b[32mhello\x1b[0m"
		expected: str = "hello"
		self.assertEqual(strings.strip_ansi(sent), expected)
