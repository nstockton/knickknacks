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

"""An implementation of UUIDv7 (RFC 9562)."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import secrets
import threading
import time
from datetime import datetime, timezone
from typing import ClassVar, Optional, Union
from uuid import UUID

# Local Modules:
from .typedef import Self


UUID_VERSION: int = 7
NIL_UUID: UUID = UUID(bytes=bytes(16))
MAX_UUID: UUID = UUID(bytes=bytes([255 for _ in range(16)]))
MAX_COUNTER: int = 0xFFF  # 12 bits.
MILLISECONDS_IN_SECONDS: int = 1000
NANOSECONDS_IN_MILLISECONDS: int = 1000000
TOTAL_LENGTH: int = 16  # The total number of bytes in UUIDv7.
TIMESTAMP_LENGTH: int = 6  # The number of bytes required to store the timestamp in milliseconds.


def get_random_counter() -> int:
	"""
	Generates a random value for use when resetting the counter.

	Returns:
		The new value.
	"""
	return secrets.randbelow(MAX_COUNTER + 1)


def get_current_milliseconds() -> int:
	"""
	Retrieves the current time in milliseconds since the Unix epoch.

	Returns:
		The milliseconds value
	"""
	return time.time_ns() // NANOSECONDS_IN_MILLISECONDS


class UUID7:  # NOQA: PLR0904
	"""A thread-safe, implementation of UUID version 7."""

	_lock: ClassVar[threading.RLock] = threading.RLock()
	_previous_milliseconds: int = get_current_milliseconds()
	_previous_counter: int = get_random_counter()

	def __init__(self, value: Optional[bytes] = None) -> None:
		"""
		Defines the constructor.

		Args:
			value: A value to generate the UUID from.

		Raises:
			ValueError: Either the version or length of the value in bytes is wrong.
		"""
		if value is not None and len(value) != TOTAL_LENGTH:
			raise ValueError(f"Expected exactly {TOTAL_LENGTH} bytes.")
		self._uuid: UUID
		if value:
			self._uuid = UUID(bytes=value)
			if self._uuid.version != UUID_VERSION:
				raise ValueError("Not a UUIDv7.")
		else:
			self._uuid = self.new().uuid

	@classmethod
	def new(cls: type[Self]) -> Self:
		"""
		Creates a new instance from the current time.

		Returns:
			The new instance.

		Raises:
			ValueError: Clock moved backwards.
		"""
		with cls._lock:
			current_milliseconds: int = get_current_milliseconds()
			if current_milliseconds < cls._previous_milliseconds:
				raise ValueError("Clock moved backwards. UUID generation aborted.")
			if current_milliseconds == cls._previous_milliseconds:
				cls._previous_counter += 1
				# The RFC suggests that if the counter reaches its maximum,
				# the implementation should wait for the next millisecond, or
				# use an alternative method, e.g., a larger counter.
				# Write a test for this later.
				if cls._previous_counter > MAX_COUNTER:  # pragma: no cover
					# Wait for the next millisecond.
					current_milliseconds += 1
					while get_current_milliseconds() < current_milliseconds:
						time.sleep(0.0001)  # Brief sleep to avoid busy-waiting.
					# Since current milliseconds changed, the previous counter should be reset.
					cls._previous_counter = get_random_counter()
			else:
				cls._previous_counter = get_random_counter()
			cls._previous_milliseconds = current_milliseconds
			return cls.from_timestamp(
				current_milliseconds / MILLISECONDS_IN_SECONDS, counter=cls._previous_counter
			)

	@property
	def uuid(self) -> UUID:
		"""The UUID."""
		return self._uuid

	@property
	def hex(self) -> str:
		"""The hex value of the UUID."""
		return self._uuid.hex

	@classmethod
	def from_datetime(cls: type[Self], value: datetime) -> Self:
		"""
		Creates a new instance from a `datetime` object.

		Args:
			value: The `datetime` object.

		Returns:
			The new instance.
		"""
		return cls.from_timestamp(value.timestamp())

	@classmethod
	def from_timestamp(cls: type[Self], value: float, *, counter: int = 0) -> Self:
		"""
		Creates a new instance from a timestamp.

		Args:
			value: The timestamp in seconds since the Unix epoch.
			counter: A number 0 through 0xFFF, used as a counter.

		Returns:
			The new instance.

		Raises:
			ValueError: Counter out of range.
		"""
		if not 0 <= counter <= MAX_COUNTER:
			raise ValueError("counter not in range 0-0xFFF.")
		value = int(value * MILLISECONDS_IN_SECONDS)  # Convert timestamp to milliseconds.
		result = bytearray()
		# Timestamp bytes.
		result.extend(value.to_bytes(length=TIMESTAMP_LENGTH, byteorder="big"))
		# Fill remaining bytes with random data.
		result.extend(secrets.token_bytes(TOTAL_LENGTH - TIMESTAMP_LENGTH))
		# The version number is in the most significant 4 bits of octet 6 I.E. bits 48 through 51 of the UUID.
		result[6] &= 0xF  # Clear first 4 bits.
		result[6] |= UUID_VERSION << 4  # Set first 4 bits to version.
		# The counter is 12 bits, split between the
		# least significant 4 bits of octet 6 and all bits of octet 7.
		# See Fixed Bit-Length Dedicated Counter, RFC 9562, Section 6.2, Method 1.
		result[6] &= ~0xF  # Clear last 4 bits. Masking with 0xF0 also works.
		result[6] |= counter >> 8  # Set last 4 bits to first 4 bits of counter.
		result[7] = counter & 0xFF  # Set all 8 bits to last 8 bits of counter.
		# The variant field consists of a variable number of the most significant bits of octet 8 of the UUID.
		# We want the RFC 4122 variant.
		# Variant RFC 4122 is 0b10xx, I.E. 8 through B.
		result[8] &= 0x3F  # Clear first 2 bits.
		result[8] |= 2 << 6  # Set first 2 bits.
		return cls.from_bytes(bytes(result))

	@classmethod
	def from_bytes(cls: type[Self], value: bytes) -> Self:
		"""
		Creates a new instance from a bytes object.

		Args:
			value: The bytes object.

		Returns:
			The new instance.
		"""
		return cls(value)

	@classmethod
	def from_hex(cls: type[Self], value: str) -> Self:
		"""
		Creates a new instance from a hex string.

		Args:
			value: The hex string.

		Returns:
			The new instance.
		"""
		return cls.from_bytes(bytes.fromhex(value))

	@classmethod
	def from_int(cls: type[Self], value: int) -> Self:
		"""
		Creates a new instance from an integer.

		Args:
			value: The integer.

		Returns:
			The new instance.
		"""
		return cls.from_bytes(int.to_bytes(value, length=TOTAL_LENGTH, byteorder="big"))

	@classmethod
	def from_uuid(cls: type[Self], value: UUID) -> Self:
		"""
		Creates a new instance from a UUID.

		Args:
			value: The UUID.

		Returns:
			The new instance.
		"""
		return cls.from_bytes(value.bytes)

	@property
	def counter(self) -> int:
		"""The counter."""
		counter_bytes = self.uuid.bytes[TIMESTAMP_LENGTH : TIMESTAMP_LENGTH + 2]
		# First 4 bits is version, remaining 12 is counter.
		return int.from_bytes(counter_bytes, byteorder="big") & 0xFFF  # The last 12 bits.

	@property
	def milliseconds(self) -> int:
		"""The time since the Unix epoch in milliseconds."""
		# You could also do this using a bitwise operation.
		"""self.uuid.int >> ((TOTAL_LENGTH - TIMESTAMP_LENGTH) * 8)"""
		return int.from_bytes(self.uuid.bytes[:TIMESTAMP_LENGTH], byteorder="big")

	@property
	def timestamp(self) -> float:
		"""The epoch time in seconds."""
		return self.milliseconds / MILLISECONDS_IN_SECONDS

	@property
	def datetime(self) -> datetime:
		"""A timezone-aware datetime in UTC from the timestamp."""
		return datetime.fromtimestamp(self.timestamp, timezone.utc)

	def __eq__(self, other: object) -> bool:
		if isinstance(other, type(self)):
			return self.uuid == other.uuid
		if isinstance(other, UUID):
			return self.uuid == other
		return False

	def __lt__(self, other: Union[Self, UUID]) -> bool:
		if isinstance(other, type(self)):
			return self.uuid < other.uuid
		if isinstance(other, UUID):
			return self.uuid < other
		return False

	def __gt__(self, other: Union[Self, UUID]) -> bool:
		if isinstance(other, type(self)):
			return self.uuid > other.uuid
		if isinstance(other, UUID):
			return self.uuid > other
		return False

	def __le__(self, other: Union[Self, UUID]) -> bool:
		if isinstance(other, type(self)):
			return self.uuid <= other.uuid
		if isinstance(other, UUID):
			return self.uuid <= other
		return False

	def __ge__(self, other: Union[Self, UUID]) -> bool:
		if isinstance(other, type(self)):
			return self.uuid >= other.uuid
		if isinstance(other, UUID):
			return self.uuid >= other
		return False

	def __hash__(self) -> int:
		return hash(self.uuid)

	def __int__(self) -> int:
		return self.uuid.int

	def __bytes__(self) -> bytes:
		return self._uuid.bytes

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self!s})"

	def __str__(self) -> str:
		return str(self.uuid)
