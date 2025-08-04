"""Class defines tokens"""

import enum


class TokenType(enum.Enum):
    """Our enum for all types of tokens."""

    EOF = -1
    NEWLINE = 0
    INTEGER = 1
    FLOAT = 2
    IDENT = 3
    STRING = 4

    # KEYWORDS
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110

    # OPERATORS
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
