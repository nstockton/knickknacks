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

"""Stuff to do with platforms."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import _imp  # NOQA: PLC2701
import inspect
import sys
from functools import cache
from pathlib import Path


@cache
def getDirectoryPath(*args: str) -> str:
	"""
	Retrieves the path of the directory where the program is located.

	If frozen, path is based on the location of the executable.
	If not frozen, path is based on the location of the module which called this function.

	Args:
		*args: Positional arguments to be passed to Path.joinpath after the directory path.

	Returns:
		The path.
	"""
	path: Path = Path(sys.executable if isFrozen() else inspect.stack()[1].filename).parent
	return str(path.joinpath(*args).resolve())


@cache
def isFrozen() -> bool:
	"""
	Determines whether the program is running from a frozen copy or from source.

	Returns:
		True if frozen, False otherwise.
	"""
	return bool(getattr(sys, "frozen", False) or hasattr(sys, "importers") or _imp.is_frozen("__main__"))


def touch(name: str) -> None:
	"""
	Touches a file.

	I.E. creates the file if it doesn't exist, or updates the modified time of the file if it does.

	Args:
		name: the file name to touch.
	"""
	path: Path = Path(name).resolve()
	path.touch()
