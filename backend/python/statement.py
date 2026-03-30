# statement.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
import re
import struct
import io
from typing import IO

from .token_ import Tokenfrom .error import Error

# ---------------------------------------------------------------------------
# Reader — wraps either a binary file or stdin, mirrors C++ Reader class
# ---------------------------------------------------------------------------

class _Reader:
    """Unified line/byte reader over a file path or a binary stream."""

    def __init__(self, source: str | IO[bytes]) -> None:
        if isinstance(source, str):
            self._file = open(source, "rb")
            self._owns = True
        else:
            self._file = source
            self._owns = False

    def __del__(self) -> None:
        if self._owns:
            self._file.close()

    def readline(self) -> str | None:
        """Read one line; return None at EOF, str (with \\n) otherwise."""
        raw = self._file.readline()
        if not raw:
            return None
        return raw.decode("utf-8", errors="replace")

    def read_bytes(self, n: int) -> list[int]:
        """Read n raw bytes, return as list of unsigned ints."""
        raw = self._file.read(n)
        return list(raw)

    def read_doubles(self, n: int) -> list[float]:
        """Read n IEEE 754 doubles (little-endian), return as list."""
        raw = self._file.read(n * 8)
        if len(raw) < n * 8:
            return []
        return list(struct.unpack(f"{n}d", raw))


# ---------------------------------------------------------------------------
# Statement
# ---------------------------------------------------------------------------

class Statement:
    """A parsed QPlot command statement, comprising tokens and inline data."""

    def __init__(self) -> None:
        self.clear()

    def clear(self) -> None:
        self._lbl: str = ""
        self._toks: list[Token] = []
        self._dat: dict[int, list[float]] = {}   # cached numeric vectors
        self._next_idx: dict[int, int] = {}       # cacheVector end indices
        self._nlines: int = 0
        # Parsing state (reset on each read)
        self._in_string: bool = False
        self._str_delim: str = ""
        self._str: str = ""
        self._lev: int = 0
        self._data_refs: list[tuple[int, str]] = []

    # --- Public read interface --------------------------------------------

    def read(self, source: str | IO[bytes],
             label: str = "") -> int:
        """Parse one statement from source. Returns number of lines read."""
        reader = _Reader(source)
        return self._read(reader, label)

    def _read(self, reader: _Reader, label: str) -> int:
        self._lbl = label
        self.clear()
        self._lbl = label  # restore after clear()

        line = reader.readline()
        if line is None or not line.endswith("\n"):
            return 0

        self._nlines = 1
        words = re.split(r"[ \t\n\r]", line)
        for w in words:
            if w or self._lev or self._in_string:
                self._process(w)

        # Continue reading if inside brackets
        while self._lev > 0:
            line = reader.readline()
            if line is None or not line.endswith("\n"):
                break
            self._nlines += 1
            words = re.split(r"[ \t\n\r]", line)
            for w in words:
                if w or self._lev or self._in_string:
                    self._process(w)

        # Resolve data references — read binary data following the text line
        for idx, desc in self._data_refs:
            self._next_idx[idx] = idx + 1
            if desc.startswith("uc"):
                # Unsigned char data, normalised to [0, 1]
                try:
                    n = int(desc[2:])
                except ValueError:
                    Error() << "Unacceptable data reference"
                    continue
                raw = reader.read_bytes(n)
                if len(raw) < n:
                    Error() << "End-of-file while reading data"
                    return 0
                self._dat[idx] = [b / 255.0 for b in raw]
            else:
                # Raw double data
                try:
                    n = int(desc)
                except ValueError:
                    Error() << "Unacceptable data reference"
                    continue
                data = reader.read_doubles(n)
                if len(data) < n:
                    Error() << "End-of-file while reading data"
                    return 0
                self._dat[idx] = data

        self._data_refs.clear()
        self._str_delim = ""
        self._str = ""
        return self._nlines

    # --- Tokenizer --------------------------------------------------------

    def _process(self, w: str) -> None:
        if self._in_string:
            idx = w.find(self._str_delim)
            if idx >= 0:
                self._str += w[:idx]
                w = w[idx + 1:]
                if w.startswith('"') or w.startswith("'"):
                    # Continuation string with new delimiter
                    self._str_delim = w[0]
                    self._process(w[1:])
                else:
                    self._toks.append(
                        Token.from_type_and_str(Token.STRING, self._str))
                    self._in_string = False
                    self._process(w)
            else:
                self._str += w + " "
        else:
            if w == "-":
                self._toks.append(Token.from_type_and_str(Token.DASH, "-"))

            elif w.startswith("["):
                self._toks.append(Token.from_type(Token.OPENBRACKET))
                self._lev += 1
                self._process(w[1:])

            elif w.startswith("("):
                self._toks.append(Token.from_type(Token.OPENPAREN))
                self._lev += 1
                self._process(w[1:])

            elif w.startswith("'") or w.startswith('"'):
                self._in_string = True
                self._str_delim = w[0]
                self._process(w[1:])

            elif w.endswith("]"):
                self._process(w[:-1])
                self._toks.append(Token.from_type(Token.CLOSEBRACKET))
                self._lev -= 1

            elif w.endswith(")"):
                self._process(w[:-1])
                self._toks.append(Token.from_type(Token.CLOSEPAREN))
                self._lev -= 1

            elif w.startswith("*"):
                desc = w[1:]
                t = Token.from_type_and_str(Token.DATAREF, desc)
                self._data_refs.append((len(self._toks), desc))
                self._toks.append(t)

            elif _is_capital(w):
                self._toks.append(Token.from_type_and_str(Token.CAPITAL, w))

            elif not w:
                pass  # ignore empty tokens

            else:
                try:
                    n = float(w)
                    self._toks.append(Token.from_number(n))
                except ValueError:
                    self._toks.append(
                        Token.from_type_and_str(Token.BAREWORD, w))

    # --- Public query interface -------------------------------------------

    def __len__(self) -> int:
        """Number of tokens — replaces C++ length()."""
        return len(self._toks)

    def __getitem__(self, idx: int) -> Token:
        """Token access by index — replaces C++ operator[]."""
        return self.token(idx)

    def token(self, idx: int) -> Token:
        """Return token at idx, or a null Token if out of range."""
        if 0 <= idx < len(self._toks):
            return self._toks[idx]
        return Token()  # null token

    def is_numeric(self, idx: int) -> bool:
        """True if token is a number, a numeric vector, or '-'."""
        if idx < 0 or idx >= len(self._toks):
            return False
        t = self._toks[idx]
        if t.typ == Token.NUMBER:
            return True
        if t.typ == Token.DASH:
            return True
        if idx in self._dat:
            return True
        if t.typ == Token.OPENBRACKET:
            return self._cache_vector(idx)
        return False

    def next_index(self, idx: int) -> int:
        """Return the index of the token after the (possibly multi-token)
        numeric value starting at idx. Returns -1 if idx is out of range."""
        if idx < 0 or idx >= len(self._toks):
            return -1
        t = self._toks[idx]
        if t.typ in (Token.NUMBER, Token.DASH):
            return idx + 1
        if self._cache_vector(idx):
            return self._next_idx[idx]
        return idx + 1

    def data(self, idx: int) -> list[float]:
        """Return numeric data at idx as a list. Only valid if is_numeric()."""
        if self._cache_vector(idx):
            return self._dat[idx]
        return []

    def label(self) -> str:
        return self._lbl

    def line_count(self) -> int:
        return self._nlines

    # --- Private cache ----------------------------------------------------

    def _cache_vector(self, idx: int) -> bool:
        """Populate _dat[idx] if possible. Returns True on success."""
        if idx in self._dat:
            return True
        if idx < 0 or idx >= len(self._toks):
            return False

        t = self._toks[idx]

        if t.typ == Token.NUMBER:
            self._dat[idx] = [t.num]
            self._next_idx[idx] = idx + 1
            return True

        if t.typ == Token.DASH:
            self._dat[idx] = [math.nan]
            self._next_idx[idx] = idx + 1
            return True

        if t.typ == Token.OPENBRACKET:
            v: list[float] = []
            i = idx
            while True:
                i += 1
                if i >= len(self._toks):
                    return False
                ti = self._toks[i]
                if ti.typ == Token.CLOSEBRACKET:
                    self._next_idx[idx] = i + 1
                    self._dat[idx] = v
                    return True
                elif ti.typ == Token.NUMBER:
                    v.append(ti.num)
                elif ti.typ == Token.DASH:
                    v.append(math.nan)
                else:
                    return False  # error — unexpected token inside bracket

        return False


# ---------------------------------------------------------------------------
# Module-level helper
# ---------------------------------------------------------------------------

def _is_capital(w: str) -> bool:
    """True if w is 1–2 uppercase ASCII letters (panel ID convention)."""
    if not w or len(w) > 2:
        return False
    return all('A' <= c <= 'Z' for c in w)
