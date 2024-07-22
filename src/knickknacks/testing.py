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
from collections.abc import Callable, Container
from typing import Any


class ContainerEmptyMixin:
	"""
	A mixin class to be used in unit tests.
	"""

	assertIsInstance: Callable[..., Any]
	assertTrue: Callable[..., Any]
	assertFalse: Callable[..., Any]

	def assertContainerEmpty(self, obj: Container[Any]) -> None:
		"""
		Asserts whether the given object is an empty container.

		Args:
			obj: The object to test.
		"""
		self.assertIsInstance(obj, Container)
		self.assertFalse(obj)

	def assertContainerNotEmpty(self, obj: Container[Any]) -> None:
		"""
		Asserts whether the given object is a non-empty container.

		Args:
			obj: The object to test.
		"""
		self.assertIsInstance(obj, Container)
		self.assertTrue(obj)
