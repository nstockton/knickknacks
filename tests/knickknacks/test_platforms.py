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
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

# Knickknacks Modules:
from knickknacks import platforms


class TestPlatforms(TestCase):
	@patch("knickknacks.platforms.isFrozen")
	def test_getDirectoryPath(self, mockIsFrozen: Mock) -> None:
		subdirectory: tuple[str, ...] = ("level1", "level2")
		frozenDirName: Path = Path(sys.executable).parent
		frozenOutput: str = str(frozenDirName.joinpath(*subdirectory).resolve())
		mockIsFrozen.return_value = True
		self.assertEqual(platforms.getDirectoryPath(*subdirectory), frozenOutput)
		platforms.getDirectoryPath.cache_clear()
		# The location of the file which called the function, I.E. this file.
		unfrozenDirName: Path = Path(__file__).parent
		unfrozenOutput: str = str(unfrozenDirName.joinpath(*subdirectory).resolve())
		mockIsFrozen.return_value = False
		self.assertEqual(platforms.getDirectoryPath(*subdirectory), unfrozenOutput)

	@patch("knickknacks.platforms._imp")
	@patch("knickknacks.platforms.sys")
	def test_getFreezer(self, mockSys: Mock, mockImp: Mock) -> None:
		mockSys.frozen = False
		del mockSys.importers
		mockImp.is_frozen.return_value = False
		self.assertFalse(platforms.isFrozen())
		platforms.isFrozen.cache_clear()
		mockImp.is_frozen.return_value = True
		self.assertTrue(platforms.isFrozen())
		platforms.isFrozen.cache_clear()
		mockImp.is_frozen.return_value = False
		mockSys.importers = True
		self.assertTrue(platforms.isFrozen())
		platforms.isFrozen.cache_clear()
		del mockSys.importers
		mockSys.frozen = True
		self.assertTrue(platforms.isFrozen())
		platforms.isFrozen.cache_clear()
		mockSys.frozen = False
		self.assertFalse(platforms.isFrozen())

	@patch("knickknacks.platforms.Path.touch")
	def test_touch(self, mockTouch: Mock) -> None:
		platforms.touch("path_1")
		mockTouch.assert_called_once()
