"""This module is the starting point of my compiler"""

from lex import Lexer


def main():
    """Runs the compiler"""

    source = "LEF foobar = 123"
    lexer = Lexer(source=source)

    while lexer.peek() != "\0":
        print(lexer.cur_char)
        lexer.next_char()


main()
