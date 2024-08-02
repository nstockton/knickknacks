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
import os
import sys
from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

# Knickknacks Modules:
from knickknacks import platforms


class TestPlatforms(TestCase):
	@patch("knickknacks.platforms.isFrozen")
	def test_getDirectoryPath(self, mockIsFrozen: Mock) -> None:
		subdirectory: tuple[str, ...] = ("level1", "level2")
		frozenDirName: str = os.path.dirname(sys.executable)
		frozenOutput: str = os.path.realpath(os.path.join(frozenDirName, *subdirectory))
		mockIsFrozen.return_value = True
		self.assertEqual(platforms.getDirectoryPath(*subdirectory), frozenOutput)
		platforms.getDirectoryPath.cache_clear()
		unfrozenDirName: str = os.path.join(os.path.dirname(platforms.__file__), os.path.pardir)
		unfrozenOutput: str = os.path.realpath(os.path.join(unfrozenDirName, *subdirectory))
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

	@patch("knickknacks.platforms.open", mock_open(read_data="data"))
	@patch("knickknacks.platforms.os")
	def test_touch(self, mockOs: Mock) -> None:
		platforms.touch("path_1")
		mockOs.utime.assert_called_once_with("path_1", None)
