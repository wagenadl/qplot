# token_.py - This file is part of QPlot
# (named token_.py to avoid shadowing Python's standard library 'token' module)

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

import enum


class Token:
    """A single lexical token from a QPlot statement."""

    class Type(enum.IntEnum):
        NONE         = 0
        BAREWORD     = 1
        CAPITAL      = 2
        NUMBER       = 3
        OPENBRACKET  = 4
        CLOSEBRACKET = 5
        OPENPAREN    = 6
        CLOSEPAREN   = 7
        STRING       = 8
        DASH         = 9
        DATAREF      = 10

    # Expose Type members directly on Token for convenience,
    # mirroring C++ Token::BAREWORD, Token::NUMBER etc.
    NONE         = Type.NONE
    BAREWORD     = Type.BAREWORD
    CAPITAL      = Type.CAPITAL
    NUMBER       = Type.NUMBER
    OPENBRACKET  = Type.OPENBRACKET
    CLOSEBRACKET = Type.CLOSEBRACKET
    OPENPAREN    = Type.OPENPAREN
    CLOSEPAREN   = Type.CLOSEPAREN
    STRING       = Type.STRING
    DASH         = Type.DASH
    DATAREF      = Type.DATAREF

    def __init__(self,
                 typ: Type = Type.NONE,
                 num: float = 0.0,
                 str_: str = "") -> None:
        self.typ = typ
        self.num = num
        self.str = str_

    # --- Factory constructors (replace C++ overloaded constructors) --------

    @classmethod
    def from_type(cls, t: "Token.Type") -> "Token":
        """Token(Type t) — type-only token with synthetic str."""
        return cls(typ=t, num=0.0, str_=f"<{int(t)}>")

    @classmethod
    def from_number(cls, n: float) -> "Token":
        """Token(double n) — numeric token."""
        return cls(typ=cls.Type.NUMBER, num=n, str_=f"#{n}")

    @classmethod
    def from_type_and_str(cls, t: "Token.Type", s: str) -> "Token":
        """Token(Type t, QString s) — typed token with explicit str."""
        return cls(typ=t, num=0.0, str_=s)

    def __repr__(self) -> str:
        return f"Token(typ={self.typ.name}, num={self.num}, str={self.str!r})"
