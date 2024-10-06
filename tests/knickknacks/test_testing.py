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
from typing import Any
from unittest import TestCase
from unittest.mock import Mock

# Knickknacks Modules:
from knickknacks import testing


class MockTestCase(Mock):
	"""A mocked version of TestCase."""

	def __init__(self, *args: Any, **kwargs: Any) -> None:
		kwargs["spec_set"] = TestCase
		kwargs["unsafe"] = True
		super().__init__(*args, **kwargs)


class ContainerEmpty(testing.ContainerEmptyMixin, MockTestCase):
	"""ContainerEmptyMixin with mocked TestCase."""


class TestTesting(TestCase):
	def test_ContainerEmptyMixin(self) -> None:
		test = ContainerEmpty()
		test.assertContainerEmpty([])
		test.assertIsInstance.assert_called_once()
		test.assertFalse.assert_called_once()
		test.reset_mock()
		test.assertContainerNotEmpty([])
		test.assertIsInstance.assert_called_once()
		test.assertTrue.assert_called_once()
