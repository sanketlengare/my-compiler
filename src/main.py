"""This module is the starting point of my compiler"""

from lex import Lexer
from token_type import TokenType


def main():
    """Runs the compiler"""

    # source = "LEF foobar = 123"
    # lexer = Lexer(source=source)

    # while lexer.peek() != "\0":
    #     print(lexer.cur_char)
    #     lexer.next_char()

    source = "123 1.23"
    lexer = Lexer(source=source)

    token = lexer.get_token()
    while token is not None and token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()


main()
