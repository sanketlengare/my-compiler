"""Class representing a Parser object"""

import sys

from .token_type import TokenType
from .lex import Lexer


class Parser:
    """Parser object controls the lexer and request a new token as needed"""

    def __init__(self, lexer):
        self.lexer = lexer

        self.curr_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def check_token(self, kind):
        """Return true if the current token matches."""

        if self.curr_token is not None:
            return kind == self.curr_token.kind
        else:
            return False

    def check_peek(self, kind):
        """Return true if the next token matches"""

        if self.peek_token is not None:
            return kind == self.peek_token.kind
        else:
            return False

    def match(self, kind):
        """Try to match current token. If not, error. Advances the current token"""

        if not self.check_token(kind) and self.curr_token is not None:
            self.abort("Expected " + kind.name + ", got " + self.curr_token.kind.name)

        self.next_token()

    def next_token(self):
        """Advances the current token"""

        self.curr_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def nl(self):
        """Requires at least one newline"""

        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def statement(self):
        """Check the first tocken to see what kind of statement this is"""

        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                # simple string
                self.next_token()
            else:
                # Expect an expression
                # self.expression()
                print("expects an expression")

        self.nl()

    def program(self):
        """Parses all the statements in the program"""

        print("PROGRAM")

        while not self.check_token(TokenType.EOF):
            self.statement()

    def abort(self, message):
        """Handle errors"""

        sys.exit("Error: " + message)
