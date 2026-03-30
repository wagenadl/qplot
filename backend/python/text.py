# text.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

from dataclasses import dataclass, field

from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QFont, QFontMetricsF, QPainter

from .factor import pt2iu
_SCRIPT_SIZE  = 0.75
_SCRIPT_SHIFT = 0.75

_SUPS = "²³¹⁰ⁱ⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ"
_SUPR = "2310i456789+−=()n"
_SUBS = "ᵢᵣᵤᵥᵦᵧᵨᵩᵪ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₔₕₖₗₘₙₚₛₜⱼ"
_SUBR = "iruvβγρφχ0123456789+-=()aeoxəhklmnpstj"


# ---------------------------------------------------------------------------
# Internal data structures
# ---------------------------------------------------------------------------

@dataclass
class _Span:
    startpos: QPointF = field(default_factory=QPointF)
    font:     QFont   = field(default_factory=QFont)
    text:     str     = ""


@dataclass
class _State:
    fontfamily: str   = "Helvetica"
    fontsize:   float = 0.0   # in internal units
    baseline:   float = 0.0
    slant:      bool  = False
    bold:       bool  = False


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _all_word(txt: str) -> bool:
    if not txt:
        return False
    return all(c.isalnum() for c in txt)


def _next_unprotected(s: str, idx: int) -> int:
    """Return index of next unprotected space/special char from idx.
    Spaces inside matched bracket/quote pairs are protected.
    Backslash escapes otherwise-pairable characters.
    Returns len(s) if nothing found."""
    pairs = "()[]{}〈〉⟨⟩«»⟪⟫⟦⟧''\u201c\u201d⌊⌋⌈⌉"
    L = len(s)
    starts: list[int] = []
    matched_start: set[int] = set()
    matched_end:   set[int] = set()

    # First pass: find matched bracket/quote pairs
    backslash = False
    for i in range(idx, L):
        if s[i] == '\\':
            backslash = not backslash
        elif backslash:
            backslash = False
            continue
        what = pairs.find(s[i])
        if what < 0:
            continue
        if (what & 1) == 0:       # opening character
            starts.append(i)
        else:                      # closing character
            for k in range(len(starts) - 1, -1, -1):
                start = starts[k]
                if pairs[what & ~1] == s[start]:
                    matched_start.add(start)
                    matched_end.add(i)
                    del starts[k:]
                    break

    # Second pass: find first unprotected space or special character
    space = " \t\n\r_^"
    prot = 0
    backslash = False
    for i in range(idx, L):
        if s[i] == '\\':
            backslash = not backslash
        if i in matched_start:
            prot += 1
        elif i in matched_end:
            prot -= 1
            if prot == 0:
                return i + 1
        elif prot == 0:
            if s[i] in space:
                return i
            if not backslash:
                what = pairs.find(s[i])
                if what > 0 and (what & 1):
                    return i
    return L


def _double_space(s: str) -> str:
    """Qt5 workaround: trailing space is cut from bbox calc."""
    return s + " " if s.endswith(" ") else s


# ---------------------------------------------------------------------------
# Text class
# ---------------------------------------------------------------------------

class Text:
    """Rich text renderer supporting super/subscripts, bold, italic."""

    def __init__(self) -> None:
        self._spans: list[_Span]  = []
        self._nextx: float        = 0.0
        self._bb:    QRectF       = QRectF()
        self._stack: list[_State] = []
        self.clear()

    def clear(self) -> None:
        self._spans = []
        self._nextx = 0.0
        self._bb    = QRectF()
        self._stack = []
        s = _State()
        s.fontfamily = "Helvetica"
        s.fontsize   = pt2iu(10)
        s.baseline   = 0.0
        s.slant      = False
        s.bold       = False
        self._stack.append(s)

    # --- Font selection (replaces two C++ setFont overloads) --------------

    def set_font_from_qfont(self, f: QFont) -> None:
        """setFont(QFont const &f)"""
        s = _State(**vars(self._stack[-1]))
        s.fontfamily = f.family()
        s.fontsize   = f.pixelSize()
        s.slant      = f.italic()
        s.bold       = f.bold()
        self._stack.append(s)

    def set_font_family(self, family: str, size: float) -> None:
        """setFont(QString family, double size)"""
        s = _State(**vars(self._stack[-1]))
        s.fontfamily = family
        s.fontsize   = size
        self._stack.append(s)

    # --- Style toggles ----------------------------------------------------

    def toggle_slant(self) -> None:
        s = _State(**vars(self._stack[-1]))
        s.slant = not s.slant
        self._stack.append(s)

    def toggle_bold(self) -> None:
        s = _State(**vars(self._stack[-1]))
        s.bold = not s.bold
        self._stack.append(s)

    def set_super(self) -> None:
        s = _State(**vars(self._stack[-1]))
        fm_base   = QFontMetricsF(_make_font(s))
        r_base    = fm_base.tightBoundingRect("x")
        s.fontsize *= _SCRIPT_SIZE
        fm_script = QFontMetricsF(_make_font(s))
        r_script  = fm_script.tightBoundingRect("0")
        s.baseline += r_base.top() - (1 - _SCRIPT_SHIFT) * r_script.top()
        self._stack.append(s)

    def set_sub(self) -> None:
        s = _State(**vars(self._stack[-1]))
        s.fontsize *= _SCRIPT_SIZE
        fm_script = QFontMetricsF(_make_font(s))
        r_script  = fm_script.tightBoundingRect("x")
        s.baseline -= _SCRIPT_SHIFT * r_script.top()
        self._stack.append(s)

    def restore(self) -> None:
        if len(self._stack) >= 2:
            self._stack.pop()

    def italic_correct(self) -> None:
        if self._stack[-1].slant and self._spans:
            sp = self._spans[-1]
            if sp.text:
                fm = QFontMetricsF(_make_font(self._stack[-1]))
                dx = fm.rightBearing(sp.text[-1])
                if dx < 0:
                    self._nextx -= dx

    # --- Text accumulation ------------------------------------------------

    def add(self, txt: str) -> None:
        t0 = txt
        txt = txt.replace("~", " ")
        if not txt:
            return
        s    = self._stack[-1]
        span = _Span()
        span.startpos = QPointF(self._nextx, s.baseline)
        span.font     = _make_font(s)

        if t0 == "\\!":
            span.text = ""
            fm = QFontMetricsF(span.font)
            self._nextx -= fm.horizontalAdvance("x") / 5
        elif t0 == "\\,":
            span.text = ""
            fm = QFontMetricsF(span.font)
            self._nextx += fm.horizontalAdvance("x") / 5
        else:
            span.text = txt

        self._spans.append(span)
        if span.text:
            fm = QFontMetricsF(span.font)
            r  = fm.tightBoundingRect(_double_space(span.text))
            self._bb = self._bb.united(r.translated(span.startpos))
            self._nextx += fm.horizontalAdvance(span.text)

    def add_interpreted(self, txt: str) -> None:
        """Add text with rich markup: * bold *, / italic /, ^ super, _ sub."""
        # Replace ASCII minus with Unicode minus sign after non-letter
        result = list(txt)
        for i, c in enumerate(result):
            if c == '-' and (i == 0 or not result[i-1].isalpha()):
                result[i] = '\u2212'
        txt = "".join(result)

        bld = ""
        idx = 0
        while idx < len(txt):
            x = txt[idx]

            if x in ("*", "/"):
                id1 = txt.find(x, idx + 1)
                if id1 >= 0 and _all_word(txt[idx+1:id1]):
                    self.add(bld);  bld = ""
                    if x == "*":
                        self.toggle_bold()
                    else:
                        self.italic_correct()
                        self.toggle_slant()
                    self.add(txt[idx+1:id1])
                    if x == "/":
                        self.italic_correct()
                    self.restore()
                    idx = id1
                else:
                    bld += x

            elif x in ("_", "^"):
                id1 = _next_unprotected(txt, idx + 1)
                self.add(bld);  bld = ""
                if x == "^":
                    self.set_super()
                else:
                    self.set_sub()
                scrpt = txt[idx+1:id1]
                if scrpt.startswith("{") and scrpt.endswith("}"):
                    scrpt = scrpt[1:-1]
                self.add_interpreted(scrpt)
                self.restore()
                idx = id1 - 1
                if idx + 1 < len(txt):
                    cls = txt[idx+1]
                    if cls in ("_", "^") and cls != x:
                        self.add("\\!")
                        self.add("\\!")

            elif x == "\\":
                nxt = txt[idx+1:idx+2]
                if nxt == "!":
                    self.add(bld);  self.add("\\!");  bld = "";  idx += 1
                elif nxt == ",":
                    self.add(bld);  self.add("\\,");  bld = "";  idx += 1
                else:
                    bld += nxt;  idx += 1

            elif x in _SUPS:
                self.add(bld);  bld = ""
                self.set_super()
                self.add(_SUPR[_SUPS.index(x)])
                self.restore()

            elif x in _SUBS:
                self.add(bld);  bld = ""
                self.set_sub()
                self.add(_SUBR[_SUBS.index(x)])
                self.restore()

            else:
                bld += x

            idx += 1
        self.add(bld)

    # --- Metrics and rendering --------------------------------------------

    def bbox(self) -> QRectF:
        return self._bb

    def width(self) -> float:
        return self._nextx

    def render(self, p: QPainter, xy0: QPointF) -> None:
        for span in self._spans:
            p.setFont(span.font)
            p.drawText(xy0 + span.startpos, span.text)


# ---------------------------------------------------------------------------
# Module-level helper (not a method — used by set_super/set_sub)
# ---------------------------------------------------------------------------

def _make_font(s: _State) -> QFont:
    f = QFont()
    f.setFamily(s.fontfamily)
    f.setPixelSize(int(s.fontsize))
    f.setBold(s.bold)
    f.setItalic(s.slant)
    f.setKerning(True)
    return f
