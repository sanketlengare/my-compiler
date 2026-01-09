"""Class representing a Parser object"""

import sys


from .token_type import TokenType
from .ast import *
from .string_token import Token


class Parser:
    """Parser object controls the lexer and request a new token as needed"""

    def __init__(self, lexer):
        self.lexer = lexer

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

        assert self.curr_token is not None
        print("PRIMARY (" + self.curr_token.text + ")")

        token = self.curr_token

        if self.check_token(TokenType.INTEGER):
            self.next_token()
            return Num(token)
        elif self.check_token(TokenType.FLOAT):
            self.next_token()
            return Float(token)
        elif self.check_token(TokenType.STRING):
            self.next_token()
            return String(token)
        elif self.check_token(TokenType.IDENT):

            if self.curr_token.text not in self.symbols:
                self.abort(
                    "Referencing variable before assignment: " + self.curr_token.text
                )

            self.next_token()
            return Var(token)
        else:
            self.abort("Unexpected token at " + self.curr_token.text)

    # Args : void
    # Returns : void
    def unary(self):
        """unary ::= ["+" | "-"] primary"""

        print("UNARY")

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            op = self.curr_token
            self.next_token()
            primary_node = self.primary()

            zero_node = Num(Token("0", TokenType.INTEGER))
            return Bin_Op(zero_node, op, primary_node)

        return self.primary()

    # Args : void
    # Returns : void
    def term(self):
        """term ::= unary {( "/" | "*") unary}"""

        print("TERM")

        left = self.unary()
        op = self.curr_token
        while self.check_token(TokenType.SLASH) or self.check_token(TokenType.ASTERISK):
            self.next_token()
            right = self.unary()
            left = Bin_Op(left, op, right)

        return left

    # Args : void
    # Returns : void
    def expression(self):
        """expression ::= term {("+" | "-") term}"""

        print("EXPRESSION")

        left = self.term()
        op = self.curr_token
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            right = self.term()
            left = Bin_Op(left, op, right)

        return left

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

        left = self.expression()
        op = self.curr_token
        if self.is_comparison_operator():
            self.next_token()
            right = self.expression()
            left = Bin_Op(left, op, right)

        else:
            if self.curr_token is not None:
                self.abort("Expected comparison operator at " + self.curr_token.text)

        return left

    def statement(self):
        """Check the first tocken to see what kind of statement this is"""

        assert self.curr_token is not None

        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                # simple string
                token = self.curr_token
                self.next_token()
                return Print(String(token))
            else:
                # Expect an expression

                exp_node = self.expression()
                self.next_token()
                return Print(exp_node)

        elif self.check_token(TokenType.IF):
            print("IF-STATEMENT")
            self.next_token()

            condition = self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            body = []

            while not self.check_token(TokenType.ENDIF):
                stm_token = self.statement()

                if stm_token is not None:
                    body.append(stm_token)

            self.match(TokenType.ENDIF)

            return If(condition, body)

        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()

            condition = self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            body = []

            while not self.check_token(TokenType.ENDWHILE):
                stm_token = self.statement()

                if stm_token is not None:
                    body.append(stm_token)

            self.match(TokenType.ENDWHILE)

            return While(condition, body)

        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()

            if self.curr_token.text in self.labels_declared:
                self.abort("Label already exists: " + self.curr_token.text)
            self.labels_declared.add(self.curr_token.text)

            token = self.curr_token
            self.match(TokenType.IDENT)

            return Label(token)

        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gotoed.add(self.curr_token.text)

            token = self.curr_token
            self.match(TokenType.IDENT)

            return Goto(token)

        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")

            self.next_token()
            if self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            name_token = self.curr_token
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            print(self.curr_token.kind)
            print(self.curr_token.text)
            expression = self.expression()

            return Let(name_token, expression)

        elif self.check_token(TokenType.INPUT):
            print("STATEMET-INPUT")
            self.next_token()

            if self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            token = self.curr_token
            self.match(TokenType.IDENT)

            return Input(token)

        # else:
        #     if self.curr_token is not None:
        #         self.abort(
        #             "Invalid statement at "
        #             + self.curr_token.text
        #             + " ("
        #             + self.curr_token.kind.name
        #             + ")"
        #         )

        self.nl()

    def program(self):
        """Parses all the statements in the program"""

        print("PROGRAM")

        statements = []

        # Handle newlines at the start of the input
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            statement_node = self.statement()

            if statement_node is not None:
                statements.append(statement_node)

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort("GOTO label undeclared: " + label)

        return Program(statements)

    def abort(self, message):
        """Handle errors"""

        raise Exception("Error: " + message)
