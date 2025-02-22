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
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

# Knickknacks Modules:
from knickknacks import platforms


class TestPlatforms(TestCase):
	@patch("knickknacks.platforms.is_frozen")
	def test_get_directory_path(self, mock_is_frozen: Mock) -> None:
		subdirectory: tuple[str, ...] = ("level1", "level2")
		frozen_dir_name: Path = Path(sys.executable).parent
		frozen_output: str = str(frozen_dir_name.joinpath(*subdirectory).resolve())
		mock_is_frozen.return_value = True
		self.assertEqual(platforms.get_directory_path(*subdirectory), frozen_output)
		platforms.get_directory_path.cache_clear()
		# The location of the file which called the function, I.E. this file.
		unfrozen_dir_name: Path = Path(__file__).parent
		unfrozen_output: str = str(unfrozen_dir_name.joinpath(*subdirectory).resolve())
		mock_is_frozen.return_value = False
		self.assertEqual(platforms.get_directory_path(*subdirectory), unfrozen_output)

	@patch("knickknacks.platforms._imp")
	@patch("knickknacks.platforms.sys")
	def test_get_freezer(self, mock_sys: Mock, mock_imp: Mock) -> None:
		mock_sys.frozen = False
		del mock_sys.importers
		mock_imp.is_frozen.return_value = False
		self.assertFalse(platforms.is_frozen())
		platforms.is_frozen.cache_clear()
		mock_imp.is_frozen.return_value = True
		self.assertTrue(platforms.is_frozen())
		platforms.is_frozen.cache_clear()
		mock_imp.is_frozen.return_value = False
		mock_sys.importers = True
		self.assertTrue(platforms.is_frozen())
		platforms.is_frozen.cache_clear()
		del mock_sys.importers
		mock_sys.frozen = True
		self.assertTrue(platforms.is_frozen())
		platforms.is_frozen.cache_clear()
		mock_sys.frozen = False
		self.assertFalse(platforms.is_frozen())

	@patch("knickknacks.platforms.Path.touch")
	def test_touch(self, mock_touch: Mock) -> None:
		platforms.touch("path_1")
		mock_touch.assert_called_once()
