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
import inspect
import os
import sys
import textwrap
from unittest import TestCase
from unittest.mock import Mock, patch

# Knickknacks Modules:
from knickknacks import utils


class TestUtils(TestCase):
	def test_get_function_field(self) -> None:
		this_function_field = inspect.currentframe()
		if this_function_field is None:
			raise TypeError("this_function_field is None.")
		this_function_name = this_function_field.f_code.co_name
		self.assertEqual(utils.get_function_field().f_code.co_name, this_function_name)
		with self.assertRaises(AttributeError):
			utils.get_function_field(sys.getrecursionlimit() * 2)

	def test_get_function_name(self) -> None:
		this_function_field = inspect.currentframe()
		if this_function_field is None:
			raise TypeError("this_function_field is None.")
		this_function_name = this_function_field.f_code.co_name
		self.assertEqual(utils.get_function_name(), this_function_name)
		self.assertEqual(utils.get_function_name(sys.getrecursionlimit() * 2), "")

	@patch("knickknacks.utils.pager")
	@patch("knickknacks.utils.shutil")
	def test_page(self, mock_shutil: Mock, mock_pager: Mock) -> None:
		cols: int = 80
		rows: int = 24
		mock_shutil.get_terminal_size.return_value = os.terminal_size((cols, rows))
		lines: list[str] = [
			"This is the first line.",
			"this is the second line.",
			"123456789 " * 10,
			"123\n567\n9 " * 10,
			"This is the third and final line.",
		]
		lines = "\n".join(lines).splitlines()
		utils.page(lines)
		text: str = "\n".join(textwrap.fill(line.strip(), cols - 1) for line in lines)
		mock_pager.assert_called_once_with(text)
