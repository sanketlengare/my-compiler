"""Lexer class to break input string into tokens"""

import sys
from string_token import Token
from token_type import TokenType


class Lexer:
    """Lexer needs to keep track of the current position in the input
    string and characters at that position"""

    def __init__(self, source):
        self.source = (
            source + "\n"
        )  # Source code. Newline to simplify lexing/ parsing the last token
        self.cur_char = ""
        self.cur_pos = -1
        self.next_char()

    def next_char(self):
        """Process the next character"""

        self.cur_pos += 1
        if self.cur_pos + 1 >= len(self.source):
            self.cur_char = "\0"  # EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek(self):
        """Return the lookahead charcter."""

        if self.cur_pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.cur_pos + 1]

    def abort(self, message):
        """Invalid token found, print error message and exit."""

        sys.exit("Lexing error. " + message)

    def skip_whitespace(self):
        """Skip whitespace except newlines, which we will use to indicate the end of a statement"""

        while self.cur_char == " " or self.cur_char == "\t" or self.cur_char == "\r":
            self.next_char()

    def skip_comment(self):
        """Skip commnets in the code."""

        if self.cur_char == "#":
            while self.cur_char != "\n":
                self.next_char()

    def get_token(self):
        """Return the next token
        Will do the work of classifying tokens"""

        self.skip_whitespace()
        self.skip_comment()
        token = None

        if self.cur_char == "+":
            token = Token(self.cur_char, TokenType.PLUS)

        elif self.cur_char == "-":
            token = Token(self.cur_char, TokenType.MINUS)

        elif self.cur_char == "*":
            token = Token(self.cur_char, TokenType.ASTERISK)

        elif self.cur_char == "/":
            token = Token(self.cur_char, TokenType.SLASH)

        elif self.cur_char == "\n":
            token = Token(self.cur_char, TokenType.NEWLINE)

        elif self.cur_char == "\0":
            token = Token(self.cur_char, TokenType.EOF)

        elif self.cur_char == "=":
            char_next = "="
            if self.peek() == char_next:
                self.next_char()
                token = Token(self.cur_char + char_next, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)

        elif self.cur_char == "<":
            char_next = "="
            if self.peek() == char_next:
                self.next_char()
                token = Token(self.cur_char + char_next, TokenType.LTEQ)

        elif self.cur_char == ">":
            char_next = "="
            if self.peek() == char_next:
                self.next_char()
                token = Token(self.cur_char + char_next, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.LT)

        elif self.cur_char == "!":
            char_next = "="
            if self.peek() == char_next:
                self.next_char()
                token = Token(self.cur_char + char_next, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.cur_char == '"':
            self.next_char()
            special_chars = ["\r", "\n", "\t", "\\", "%"]
            start_pos = self.cur_pos

            while self.cur_char != '"':
                if self.cur_char in special_chars:
                    self.abort("Illegal character in string")
                self.next_char()

            token_text = self.source[start_pos : self.cur_pos]
            token = Token(token_text, TokenType.STRING)

        elif self.cur_char.isdigit():
            start_pos = self.cur_pos

            while self.peek().isdigit():
                self.next_char()

            if self.peek() == ".":
                self.next_char()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number")

                while self.peek().isdigit():
                    self.next_char()

                token_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(token_text, TokenType.FLOAT)

            else:
                token_text = self.source[start_pos : self.cur_pos + 1]
                token = Token(token_text, TokenType.INTEGER)

        else:
            self.abort("Unknown token: " + self.cur_char)
            return

        self.next_char()
        return token
