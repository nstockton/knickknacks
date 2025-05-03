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

"""Stuff to do with strings."""

# Future Modules:
from __future__ import annotations

# Built-in Modules:
import re
import textwrap
from collections.abc import Callable, Sequence
from typing import Any, Optional, Union

# Local Modules:
from .typedef import BytesOrStrType, RePatternType


# Regex from https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
ANSI_REGEX: RePatternType = re.compile(
	r"""
		\x1B  # ESC.
		(?:  # 7-bit C1 Fe, except CSI.
			[@-Z\\-_]
		|  # Or [ for CSI, followed by a control sequence.
			\[
			[0-?]*  # Parameter bytes.
			[ -/]*  # Intermediate bytes.
			[@-~]  # Final byte.
		)
	""",
	flags=re.VERBOSE,
)
INDENT_REGEX: RePatternType = re.compile(r"^(?P<indent>\s*)(?P<text>.*)", flags=re.UNICODE)
WHITE_SPACE_REGEX: RePatternType = re.compile(r"\s+", flags=re.UNICODE)
# Use negative look-ahead to exclude the space character from the \s character class.
# Another way to accomplish this would be to use negation (I.E. [^\S ]+).
WHITE_SPACE_EXCEPT_SPACE_REGEX: RePatternType = re.compile(r"(?:(?![ ])\s+)", flags=re.UNICODE)


def camel_case(text: str, delimiter: str) -> str:
	"""
	Converts text to camel case.

	Args:
		text: The text to be converted.
		delimiter: The delimiter between words.

	Returns:
		The text in camel case.
	"""
	words = text.split(delimiter)
	return "".join((*map(str.lower, words[:1]), *map(str.title, words[1:])))


def format_docstring(
	function_or_string: Union[str, Callable[..., Any]], width: int = 79, prefix: Optional[str] = None
) -> str:
	"""
	Formats a docstring for displaying.

	Args:
		function_or_string: The function containing the docstring, or the docstring its self.
		width: The number of characters to word wrap each line to.
		prefix: One or more characters to use for indention.

	Returns:
		The formatted docstring.
	"""
	docstring = (
		getattr(function_or_string, "__doc__", "") if callable(function_or_string) else function_or_string
	)
	# Remove any empty lines from the beginning, while keeping indention.
	docstring = docstring.lstrip("\r\n")
	match = INDENT_REGEX.search(docstring)
	if match is not None and not match.group("indent"):
		# The first line was not indented.
		# Prefix the first line with the white space from the subsequent, non-empty
		# line with the least amount of indention.
		# This is needed so that textwrap.dedent will work.
		docstring = min_indent("\n".join(docstring.splitlines()[1:])) + docstring
	docstring = textwrap.dedent(docstring)  # Remove common indention from lines.
	docstring = docstring.rstrip()  # Remove trailing white space from the end of the docstring.
	# Word wrap long lines, while maintaining existing structure.
	wrapped_lines = []
	indent_level = 0
	last_indent = ""
	for line in docstring.splitlines():
		match = INDENT_REGEX.search(line)
		if match is None:  # pragma: no cover
			continue
		indent, text = match.groups()
		if len(indent) > len(last_indent):
			indent_level += 1
		elif len(indent) < len(last_indent):
			indent_level -= 1
		last_indent = indent
		line_prefix = prefix * indent_level if prefix else indent
		lines = textwrap.wrap(
			text, width=width - len(line_prefix), break_long_words=False, break_on_hyphens=False
		)
		wrapped_lines.append(line_prefix + f"\n{line_prefix}".join(lines))
	# Indent docstring lines with the prefix.
	return textwrap.indent("\n".join(wrapped_lines), prefix=prefix or "")


def has_white_space(text: str) -> bool:
	"""
	Determines if string contains white space.

	Args:
		text: The text to process.

	Returns:
		True if found, False otherwise.
	"""
	return WHITE_SPACE_REGEX.search(text) is not None


def has_white_space_except_space(text: str) -> bool:
	"""
	Determines if string contains white space other than space.

	Args:
		text: The text to process.

	Returns:
		True if found, False otherwise.
	"""
	return WHITE_SPACE_EXCEPT_SPACE_REGEX.search(text) is not None


def min_indent(text: str) -> str:
	"""
	Retrieves the indention characters from the line with the least indention.

	Args:
		text: the text to process.

	Returns:
		The indention characters of the line with the least amount of indention.
	"""
	lines = []
	for line in text.splitlines():
		if line.strip("\r\n"):
			match = INDENT_REGEX.search(line)
			if match is not None:
				lines.append(match.group("indent"))
	return min(lines, default="", key=len)


def multi_replace(data: BytesOrStrType, replacements: Sequence[Sequence[BytesOrStrType]]) -> BytesOrStrType:
	"""
	Performs multiple replacement operations on a string or bytes-like object.

	Args:
		data: The text to perform the replacements on.
		replacements: A sequence of tuples, each containing the text to match and the replacement.

	Returns:
		The text with all the replacements applied.
	"""
	for old, new in replacements:
		data = data.replace(old, new)
	return data


def regex_fuzzy(text: Union[str, Sequence[str]]) -> str:
	"""
	Creates a regular expression matching all or part of a string or sequence.

	Args:
		text: The text to be converted.

	Returns:
		A regular expression string matching all or part of the text.

	Raises:
		TypeError: If text is neither a string nor sequence of strings.
	"""
	if not isinstance(text, (str, Sequence)):
		raise TypeError("Text must be either a string or sequence of strings.")
	if not text:
		return ""
	if isinstance(text, str):
		return "(".join(list(text)) + ")?" * (len(text) - 1)
	return "|".join("(".join(list(item)) + ")?" * (len(item) - 1) for item in text)


def remove_white_space(text: str) -> str:
	"""
	Removes all white space characters.

	Args:
		text: The text to process.

	Returns:
		The simplified version of the text.
	"""
	return WHITE_SPACE_REGEX.sub("", text)


def remove_white_space_except_space(text: str) -> str:
	"""
	Removes all white space characters except for space.

	Args:
		text: The text to process.

	Returns:
		The simplified version of the text.
	"""
	return WHITE_SPACE_EXCEPT_SPACE_REGEX.sub("", text)


def simplified(text: str) -> str:
	"""
	Replaces one or more consecutive white space characters with a single space, and trims beginning and end.

	Args:
		text: The text to process.

	Returns:
		The simplified version of the text.
	"""
	return WHITE_SPACE_REGEX.sub(" ", text).strip()


def strip_ansi(text: str) -> str:
	"""
	Strips ANSI escape sequences from text.

	Args:
		text: The text to strip ANSI sequences from.

	Returns:
		The text with ANSI escape sequences stripped.
	"""
	return ANSI_REGEX.sub("", text)
