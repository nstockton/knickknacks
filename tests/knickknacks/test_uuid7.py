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
from datetime import datetime, timezone
from unittest import TestCase, mock
from uuid import UUID, uuid4

# Knickknacks Modules:
from knickknacks.uuid7 import (
	MAX_COUNTER,
	MILLISECONDS_IN_SECONDS,
	NANOSECONDS_IN_MILLISECONDS,
	UUID7,
	get_current_milliseconds,
	get_random_counter,
)


DEMO_NANOSECONDS: int = 1732780871216430300
DEMO_MILLISECONDS: int = DEMO_NANOSECONDS // NANOSECONDS_IN_MILLISECONDS
DEMO_TIMESTAMP: float = DEMO_MILLISECONDS / MILLISECONDS_IN_SECONDS
DEMO_COUNTER: int = 1261
DEMO_DATETIME: datetime = datetime.fromtimestamp(DEMO_TIMESTAMP, timezone.utc)
DEMO_HEX: str = "019371c9ce3074edbf104b4d2b846424"
DEMO_UUID: UUID = UUID(hex=DEMO_HEX)


@mock.patch("knickknacks.uuid7.time.time_ns", mock.Mock(return_value=DEMO_NANOSECONDS))
class TestUUID7(TestCase):
	@mock.patch("knickknacks.uuid7.secrets.randbelow")
	def test_get_random_counter(self, mock_randbelow: mock.Mock) -> None:
		get_random_counter()
		mock_randbelow.assert_called_once_with(MAX_COUNTER + 1)

	def test_get_current_milliseconds(self) -> None:
		self.assertEqual(get_current_milliseconds(), DEMO_NANOSECONDS // NANOSECONDS_IN_MILLISECONDS)

	def test_init_when_invalid_value_given(self) -> None:
		with self.assertRaises(ValueError):
			UUID7(b"12345")

	def test_init_when_invalid_version_given(self) -> None:
		with self.assertRaises(ValueError):
			UUID7(uuid4().bytes)

	def test_init_when_valid_value_given(self) -> None:
		self.assertEqual(UUID7(DEMO_UUID.bytes), DEMO_UUID)

	def test_init_when_no_value_given(self) -> None:
		with mock.patch.object(UUID7, "new") as mock_new:
			mock_new.return_value.uuid = DEMO_UUID
			self.assertEqual(UUID7(), DEMO_UUID)
			mock_new.assert_called_once_with()

	@mock.patch("knickknacks.uuid7.get_current_milliseconds")
	def test_new(self, mock_get_current_milliseconds: mock.Mock) -> None:
		# I should improve this test later.
		mock_get_current_milliseconds.return_value = UUID7._previous_milliseconds - 1  # NOQA: SLF001
		with self.assertRaises(ValueError):
			UUID7.new()  # Clock moved backwards.
		mock_get_current_milliseconds.return_value = UUID7._previous_milliseconds  # NOQA: SLF001
		UUID7.new()
		mock_get_current_milliseconds.return_value = UUID7._previous_milliseconds + 1  # NOQA: SLF001
		UUID7.new()

	def test_properties(self) -> None:
		instance = UUID7(DEMO_UUID.bytes)
		self.assertEqual(instance.counter, DEMO_COUNTER)
		self.assertEqual(instance.datetime, DEMO_DATETIME)
		self.assertEqual(instance.hex, DEMO_HEX)
		self.assertEqual(instance.milliseconds, DEMO_MILLISECONDS)
		self.assertEqual(instance.timestamp, DEMO_TIMESTAMP)
		self.assertEqual(instance.uuid, DEMO_UUID)

	def test_from_datetime(self) -> None:
		self.assertEqual(UUID7.from_datetime(DEMO_DATETIME).datetime, DEMO_DATETIME)

	def test_from_timestamp_when_invalid_counter_given(self) -> None:
		with self.assertRaises(ValueError):
			UUID7.from_timestamp(DEMO_TIMESTAMP, counter=-1)
		with self.assertRaises(ValueError):
			UUID7.from_timestamp(DEMO_TIMESTAMP, counter=MAX_COUNTER + 1)

	def test_from_timestamp_when_valid_value_given(self) -> None:
		self.assertEqual(UUID7.from_timestamp(DEMO_TIMESTAMP).timestamp, DEMO_TIMESTAMP)

	def test_from_bytes(self) -> None:
		self.assertEqual(UUID7.from_bytes(DEMO_UUID.bytes), DEMO_UUID)

	def test_from_hex(self) -> None:
		self.assertEqual(UUID7.from_hex(DEMO_HEX), DEMO_UUID)

	def test_from_int(self) -> None:
		self.assertEqual(UUID7.from_int(DEMO_UUID.int), DEMO_UUID)

	def test_from_uuid(self) -> None:
		self.assertEqual(UUID7.from_uuid(DEMO_UUID), DEMO_UUID)

	def test_operators(self) -> None:
		first = UUID7.from_timestamp(DEMO_TIMESTAMP)
		second = UUID7.from_timestamp(DEMO_TIMESTAMP + 1)
		# Equal.
		self.assertEqual(first, first)
		self.assertEqual(first, first.uuid)
		self.assertNotEqual(first, object)
		# Less than.
		self.assertLess(first, second)
		self.assertLess(first, second.uuid)
		self.assertFalse(first < object)  # type: ignore[operator]
		# Less than or equal to.
		self.assertLessEqual(first, second)
		self.assertLessEqual(first, second.uuid)
		self.assertFalse(first <= object)  # type: ignore[operator]
		# Greater than.
		self.assertGreater(second, first)
		self.assertGreater(second, first.uuid)
		self.assertFalse(first > object)  # type: ignore[operator]
		# Greater than or equal to.
		self.assertGreaterEqual(second, first)
		self.assertGreaterEqual(second, first.uuid)
		self.assertFalse(first >= object)  # type: ignore[operator]

	def test_hashable(self) -> None:
		self.assertEqual(hash(UUID7.from_uuid(DEMO_UUID)), hash(DEMO_UUID))

	def test_int(self) -> None:
		self.assertEqual(int(UUID7.from_uuid(DEMO_UUID)), DEMO_UUID.int)

	def test_bytes(self) -> None:
		self.assertEqual(bytes(UUID7.from_uuid(DEMO_UUID)), DEMO_UUID.bytes)
