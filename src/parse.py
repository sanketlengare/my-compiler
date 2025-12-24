"""Class representing a Parser object"""

import sys

from .token_type import TokenType


class Parser:
    """Parser object controls the lexer and request a new token as needed"""

    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labels_declared = set()
        self.labels_gotoed = set()

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

    def primary(self):
        """primary ::= integer : ident"""

        if self.curr_token is not None:
            print("PRIMARY (" + self.curr_token.text + ")")

        if self.check_token(TokenType.INTEGER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):

            if self.curr_token and self.curr_token.text not in self.symbols:
                self.abort(
                    "Referencing variable before assignment: " + self.curr_token.text
                )

            self.next_token()
        else:
            if self.curr_token is not None:
                self.abort("Unexpected token at " + self.curr_token.text)

    # Args : void
    # Returns : void
    def unary(self):
        """unary ::= ["+" | "-"] primary"""

        print("UNARY")

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    # Args : void
    # Returns : void
    def term(self):
        """term ::= unary {( "/" | "*") unary}"""

        print("TERM")

        self.unary()
        while self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.next_token()
            self.unary()

    # Args : void
    # Returns : void
    def expression(self):
        """expression ::= term {("+" | "-") term}"""

        print("EXPRESSION")

        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    def is_comparison_operator(self):
        """Return true if the current token is a comparison operator"""

        return (
            self.check_token(TokenType.EQ)
            or self.check_token(TokenType.NOTEQ)
            or self.check_token(TokenType.GT)
            or self.check_token(TokenType.GTEQ)
            or self.check_token(TokenType.LT)
            or self.check_token(TokenType.LTEQ)
        )

    def comparison(self):
        """comparison ::= expression ((== | != | > | >= | < | <=) expression)"""

        print("COMPARISON")

        self.expression()
        if self.is_comparison_operator():
            self.next_token()
            self.expression()

        else:
            if self.curr_token is not None:
                self.abort("Expected comparison operator at " + self.curr_token.text)

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
                self.expression()

        elif self.check_token(TokenType.IF):
            print("IF-STATEMENT")
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)

        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()

            if self.curr_token:
                if self.curr_token.text in self.labels_declared:
                    self.abort("Label already exists: " + self.curr_token.text)
                self.labels_declared.add(self.curr_token.text)

            self.match(TokenType.IDENT)

        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            if self.curr_token:
                self.labels_gotoed.add(self.curr_token.text)
            self.match(TokenType.IDENT)

        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")

            self.next_token()
            if self.curr_token and self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.check_token(TokenType.INPUT):
            print("STATEMET-INPUT")
            self.next_token()

            if self.curr_token and self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            self.match(TokenType.IDENT)

        else:
            if self.curr_token is not None:
                self.abort(
                    "Invalid statement at "
                    + self.curr_token.text
                    + " ("
                    + self.curr_token.kind.name
                    + ")"
                )

        self.nl()

    def program(self):
        """Parses all the statements in the program"""

        print("PROGRAM")

        # Handle newlines at the start of the input
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort("GOTO label undeclared: " + label)

    def abort(self, message):
        """Handle errors"""

        sys.exit("Error: " + message)
