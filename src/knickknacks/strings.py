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
import re
import textwrap
from collections.abc import Callable, Sequence
from typing import Any, Optional, Union

# Local Modules:
from .typedef import REGEX_PATTERN, BytesOrStr


ANSI_COLOR_REGEX: REGEX_PATTERN = re.compile(r"\x1b\[[\d;]+m")
INDENT_REGEX: REGEX_PATTERN = re.compile(r"^(?P<indent>\s*)(?P<text>.*)", flags=re.UNICODE)
XML_ATTRIBUTE_REGEX: REGEX_PATTERN = re.compile(r"([\w-]+)(\s*=+\s*('[^']*'|\"[^\"]*\"|(?!['\"])[^\s]*))?")
WHITE_SPACE_REGEX: REGEX_PATTERN = re.compile(r"\s+", flags=re.UNICODE)


def camelCase(text: str, delimiter: str) -> str:
	"""
	converts text to camel case.

	Args:
		text: The text to be converted.
		delimiter: The delimiter between words.

	Returns:
		The text in camel case.
	"""
	words = text.split(delimiter)
	return "".join((*map(str.lower, words[:1]), *map(str.title, words[1:])))


def formatDocString(
	functionOrString: Union[str, Callable[..., Any]], width: int = 79, prefix: Optional[str] = None
) -> str:
	"""
	Formats a docstring for displaying.

	Args:
		functionOrString: The function containing the docstring, or the docstring its self.
		width: The number of characters to word wrap each line to.
		prefix: One or more characters to use for indention.

	Returns:
		The formatted docstring.
	"""
	if callable(functionOrString):  # It's a function.
		docString = getattr(functionOrString, "__doc__") or ""
	else:  # It's a string.
		docString = functionOrString
	# Remove any empty lines from the beginning, while keeping indention.
	docString = docString.lstrip("\r\n")
	match = INDENT_REGEX.search(docString)
	if match is not None and not match.group("indent"):
		# The first line was not indented.
		# Prefix the first line with the white space from the subsequent, non-empty
		# line with the least amount of indention.
		# This is needed so that textwrap.dedent will work.
		docString = minIndent("\n".join(docString.splitlines()[1:])) + docString
	docString = textwrap.dedent(docString)  # Remove common indention from lines.
	docString = docString.rstrip()  # Remove trailing white space from the end of the docstring.
	# Word wrap long lines, while maintaining existing structure.
	wrappedLines = []
	indentLevel = 0
	lastIndent = ""
	for line in docString.splitlines():
		match = INDENT_REGEX.search(line)
		if match is None:  # pragma: no cover
			continue
		indent, text = match.groups()
		if len(indent) > len(lastIndent):
			indentLevel += 1
		elif len(indent) < len(lastIndent):
			indentLevel -= 1
		lastIndent = indent
		linePrefix = prefix * indentLevel if prefix else indent
		lines = textwrap.wrap(
			text, width=width - len(linePrefix), break_long_words=False, break_on_hyphens=False
		)
		wrappedLines.append(linePrefix + f"\n{linePrefix}".join(lines))
	docString = "\n".join(wrappedLines)
	docString = textwrap.indent(
		docString, prefix=prefix if prefix is not None else ""
	)  # Indent docstring lines with the prefix.
	return docString


def getXMLAttributes(text: str) -> dict[str, Union[str, None]]:
	"""
	Extracts XML attributes from a tag.

	The supplied string must only contain attributes, not the tag name.

		Note:
			Adapted from the html.parser module of the Python standard library.

	Args:
		text: The text to be parsed.

	Returns:
		The extracted attributes.
	"""
	attributes: dict[str, Union[str, None]] = {}
	for name, rest, value in XML_ATTRIBUTE_REGEX.findall(text):
		if not rest:
			value = None
		elif value[:1] == "'" == value[-1:] or value[:1] == '"' == value[-1:]:
			value = value[1:-1]
		attributes[name.lower()] = value
	return attributes


def minIndent(text: str) -> str:
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


def regexFuzzy(text: Union[str, Sequence[str]]) -> str:
	"""
	Creates a regular expression matching all or part of a string or sequence.

	Args:
		text: The text to be converted.

	Returns:
		A regular expression string matching all or part of the text.
	"""
	if not isinstance(text, (str, Sequence)):
		raise TypeError("Text must be either a string or sequence of strings.")
	elif not text:
		return ""
	elif isinstance(text, str):
		return "(".join(list(text)) + ")?" * (len(text) - 1)
	else:
		return "|".join("(".join(list(item)) + ")?" * (len(item) - 1) for item in text)


def removePrefix(text: BytesOrStr, prefix: BytesOrStr) -> BytesOrStr:
	"""Backport of `removeprefix` from PEP-616 (Python 3.9+)"""
	if text.startswith(prefix):
		return text[len(prefix) :]
	else:
		return text


def removeSuffix(text: BytesOrStr, suffix: BytesOrStr) -> BytesOrStr:
	"""Backport of `removesuffix` from PEP-616 (Python 3.9+)"""
	if suffix and text.endswith(suffix):
		return text[: -len(suffix)]
	else:
		return text


def simplified(text: str) -> str:
	"""
	Replaces one or more consecutive white space characters with a single space.

	Args:
		text: The text to process.

	Returns:
		The simplified version of the text.
	"""
	return WHITE_SPACE_REGEX.sub(" ", text).strip()


def stripAnsi(text: str) -> str:
	"""
	Strips ANSI escape sequences from text.

	Args:
		text: The text to strip ANSI sequences from.

	Returns:
		The text with ANSI escape sequences stripped.
	"""
	return ANSI_COLOR_REGEX.sub("", text)
